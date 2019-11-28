from datetime import datetime

from django.db import models
from django.db.models import Model, QuerySet
from django.utils.timezone import make_aware
from lxml import etree  # TODO: move all internal work with xml to separate module


class Xsd(Model):
    rule = models.TextField()

    def is_valid(self, payload):
        res = False
        try:
            xmlschema_doc = etree.fromstring(self.rule.encode('utf-8'))
            xmlschema = etree.XMLSchema(xmlschema_doc)
            xml_doc = etree.fromstring(payload.encode('utf-8'))
            res = xmlschema.validate(xml_doc)
            # TODO: add logging of xmlschema.error_log if validation is False
        except Exception:
            # TODO: add logging
            pass
        return res


class RawEntityQuerySet(QuerySet):
    def create(self, payload):
        is_valid = Xsd.objects.first().is_valid(payload)  # note: xsd could be filtered
        raw_entity = super().create(payload=payload, is_valid=is_valid)

        if is_valid:
            try:
                self.create_entity_from_raw(raw_entity)
            except Exception:
                # TODO: add appropriate error handling
                raise
        return raw_entity

    @staticmethod
    def create_entity_from_raw(raw_entity):
        root = etree.fromstring(raw_entity.payload)
        entity_name = root.xpath('/Body/Entity/Name')[0].text
        phones = root.xpath('/Body/Entity/Phone')[0].text.split(';')
        emails = root.xpath('/Body/Entity/Email')[0].text.split(';')

        services = []
        for service in root.xpath('/Body/Entity/Services/*'):
            s = {
                'name': service.xpath('Name')[0].text,
                'is_main': service.attrib['is_main'] == 'true',
                'available_from': convert_dt(service.xpath('Availability/From')[0].text),
                'available_to': convert_dt(service.xpath('Availability/To')[0].text),
            }
            services.append(s)

        # TODO: is valid if any create failed? should it in transaction?
        entity = Entity.objects.create(raw_entity=raw_entity, name=entity_name)
        [Email.objects.create(entity=entity, email=email) for email in emails]
        [Phone.objects.create(entity=entity, phone=phone) for phone in phones]
        [Service.objects.create(entity=entity, name=s['name'], is_main=s['is_main'],
                                available_from=s['available_from'], available_to=s['available_to'])
         for s in services]


def convert_dt(dt_str):
    # TODO: move
    dt_obj = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    return make_aware(dt_obj)


class RawEntity(Model):
    payload = models.TextField()
    is_valid = models.BooleanField(default=False)
    objects = RawEntityQuerySet.as_manager()


class Entity(Model):
    name = models.TextField()  # TODO: use CharField with appropriate max_length
    raw_entity = models.OneToOneField(RawEntity, on_delete=models.DO_NOTHING)


class Email(Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    email = models.CharField(max_length=256)  # TODO: check max_length by rtfm


class Phone(Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    phone = models.CharField(max_length=256)  # TODO: check max_length by rtfm
    is_mobile = models.BooleanField(default=None, null=True)


class Service(Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    name = models.TextField()
    is_main = models.BooleanField()
    available_from = models.DateTimeField(null=True, blank=True)
    available_to = models.DateTimeField(null=True, blank=True)
