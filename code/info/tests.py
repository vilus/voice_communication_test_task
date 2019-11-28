import pytest

from info.models import RawEntity


pytestmark = pytest.mark.django_db


VALID_XML = '''\
<?xml version="1.0" ?>
<Body>
  <Entity>
    <Name>Name_1</Name>
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
</Body>'''  # TODO: move to common conftest.py


def test_create():
    raw_entry = RawEntity.objects.create(VALID_XML)
    assert raw_entry.is_valid

    entity = raw_entry.entity
    assert entity.name == 'Name_1'

    emails = entity.email_set.all()
    assert emails.count() == 2
    assert emails.filter(email='login@domain.com').exists()
    assert emails.filter(email='login2@domain.com').exists()

    phones = entity.phone_set.all()
    assert phones.count() == 2
    assert phones.filter(phone='+77772347122').exists()
    assert phones.filter(phone='89999999999').exists()

    services = entity.service_set.all()
    assert services.count() == 2
    assert services.filter(name='Service', is_main=True).exists()
    # TODO: check datetime
    assert services.filter(name='Service 2', is_main=False).exists()


def test_create_invalid_xml():
    raw_entry = RawEntity.objects.create(
        VALID_XML.replace('<Phone>+77772347122;89999999999</Phone>', '<Phone>+777</Phone>')
    )
    assert raw_entry.is_valid is False

    assert hasattr(raw_entry, 'entity') is False
