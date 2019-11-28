import sys
import os
import logging
import queue
import signal
import threading
import time
import random

import configargparse
import django

from django.db import transaction, DatabaseError


MAX_RECORDS = 1024
STOP = object()
RUN = object()


p = configargparse.ArgParser(default_config_files=['*/phones_processing.ini'])
p.add_argument('-s', '--settings', env_var='DJANGO_SETTINGS_MODULE',
               default='project.settings', help='django settings')
p.add_argument('-p', '--parallel', default=8, type=int,
               help='count of parallel phone processors')
p.add_argument('-i', '--interval', default=30, type=int,
               help='interval of polling new phones')
p.add_argument('-v', '--verbose', action='store_true')


class GracefulInterruptHandler:
    def __init__(self, signals=(signal.SIGINT, signal.SIGTERM)):
        self.signals = signals
        self.original_handlers = {}
        self.interrupted = False
        self.released = False

    def __enter__(self):
        for sig in self.signals:
            self.original_handlers[sig] = signal.getsignal(sig)
            signal.signal(sig, self.handler)

        return self

    # noinspection PyUnusedLocal
    def handler(self, signum, frame):
        self.release()
        self.interrupted = True

    def __exit__(self, exception_type, exception_value, traceback):
        self.release()

    def release(self):
        if self.released:
            return

        for sig in self.signals:
            signal.signal(sig, self.original_handlers[sig])

        self.released = True


def set_logging(verbose):
    level = logging.WARNING
    if verbose:
        level = logging.DEBUG
    logging.basicConfig(level=level, format='%(asctime)s %(threadName)s: %(message)s')


def django_setup(settings):
    sys.path.append(os.path.abspath('./'))  # TODO: move to conf
    os.environ['DJANGO_SETTINGS_MODULE'] = settings
    django.setup()


def get_new_phones_ids():
    from info.models import Phone  # TODO: find out conveninent way
    with transaction.atomic():
        qs = Phone.objects.select_for_update(skip_locked=True)
        qs = qs.filter(is_mobile=None).values_list('id', flat=True)[:MAX_RECORDS]
        return list(qs)


def set_mobile_flag(phone_id):
    from info.models import Phone
    with transaction.atomic():
        try:
            phone = Phone.objects.select_for_update(nowait=True).get(pk=phone_id, is_mobile=None)
            phone.is_mobile = is_mobile(phone.phone)
            phone.save()
        except (DatabaseError, Phone.DoesNotExist):  # locked or already set
            logging.exception('exeption in set_mobile_flag')
            pass


def is_mobile(phone):
    if phone.startswith('8') and len(phone) == 11:
        return True
    if phone.startswith('+7') and len(phone) == 12:
        return True
    return False


def clean_q(q):
    while not q.empty():
        try:
            q.get(block=False)
        except queue.Empty:
            continue
        q.task_done()


def ticker(in_q, out_q, interval):
    started = False  # note: its workaround
    while True:
        try:
            income = in_q.get(timeout=interval, block=started)
        except queue.Empty:
            started = True
            logging.debug('send RUN')
            out_q.put(RUN)
            continue

        if income is STOP:
            logging.debug('send STOP')
            out_q.put(STOP)
            break


def producer(in_q, out_q):
    while True:
        income = in_q.get()
        if income is STOP:
            logging.debug('send STOP')
            out_q.put(STOP)
            break

        try:
            phones_ids = get_new_phones_ids()
        except Exception:
            logging.exception('got expection in producer')
            continue

        random.shuffle(phones_ids)

        clean_q(out_q)
        for p_id in phones_ids:
            out_q.put(p_id)
        # TODO: detect stall by out_q size


def consumer(in_q):
    while True:
        income = in_q.get()
        if income is STOP:
            logging.debug('send STOP')
            in_q.put(STOP)
            break

        logging.debug(f'got phone_id {income}')
        try:
            set_mobile_flag(income)
        except Exception:
            logging.exception(f'got exception in consumer on phone_id {income}')
            continue


def main():
    options = p.parse_args()
    set_logging(options.verbose)
    django_setup(options.settings)

    ticker_in_q = queue.Queue()
    ticker_out_q = queue.Queue()
    producer_out_q = queue.Queue()

    ticker_t = threading.Thread(target=ticker, name='ticker',
                                args=(ticker_in_q, ticker_out_q, options.interval), daemon=False)
    producer_t = threading.Thread(target=producer, name='producer',
                                  args=(ticker_out_q, producer_out_q), daemon=False)
    pool = [threading.Thread(target=consumer, args=(producer_out_q, ), daemon=False)
            for _ in range(options.parallel)]
    pool.extend([producer_t, ticker_t])

    [t.start() for t in pool]
    # TODO: find out why `ticker_in_q.put(RUN)` does not work from here (and del workaround in ticker)
    with GracefulInterruptHandler() as h:
        while True:
            if h.interrupted:
                ticker_in_q.put(STOP)
                break
            time.sleep(1)

    [t.join() for t in pool]


if __name__ == '__main__':
    main()
