import requests
import configargparse
import logging


p = configargparse.ArgParser()
p.add_argument('-c', '--count', type=int,
               default=10_000, help='count of entity')
p.add_argument('-v', '--verbose', action='store_true')
p.add_argument('-u', '--url', default='http://srv:8080/api/v1/raw_entity/', type=str, help='url of entity')
# note: slash trailing!


VALID_XML = '''\
<?xml version="1.0" ?>
<Body>
  <Entity>
    <Name>Name</Name>
    <Phone>+77772347122;89999999999</Phone>
    <Email>login@domain.com;login2@domain.com</Email>
    <Services>
      <Service is_main="true">
        <Name>Service</Name>
        <Availability>
          <From>2019-01-01 00:00:00</From>
          <To>2019-12-01 23:59:59</To>
        </Availability>
      </Service>
      <Service is_main="false">
        <Name>Service 2</Name>
        <Availability>
          <From>2019-02-01 00:00:00</From>
          <To>2019-11-01 23:59:59</To>
        </Availability>
      </Service>
    </Services>
  </Entity>
</Body>'''


def set_logging(verbose):
    level = logging.WARNING
    if verbose:
        level = logging.DEBUG
    logging.basicConfig(level=level, format='%(asctime)s: %(message)s')


def send_entity(url, payload):
    try:
        res = requests.post(url, json={'payload': payload}, timeout=5)
        res.raise_for_status()
    except Exception:
        logging.exception('failed to send entity')


def main():
    options = p.parse_args()
    set_logging(options.verbose)

    [send_entity(options.url, VALID_XML) for _ in range(options.count)]


if __name__ == '__main__':
    main()
