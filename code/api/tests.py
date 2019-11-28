import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


pytestmark = pytest.mark.django_db


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
</Body>'''  # TODO: move to common conftest.py


@pytest.fixture
def api_client():
    return APIClient()


def test_api_create(api_client):
    resp = api_client.post(
        reverse('rawentity-list'),
        {
            'payload': VALID_XML
        },
        format='json'
    )
    assert resp.status_code == 201
    assert resp.data['payload'] == VALID_XML
    assert resp.data['is_valid']


@pytest.mark.parametrize(
    'payload', [
         '<?xml version="1.0" ?><body>',
         VALID_XML.replace('<Phone>+77772347122;89999999999</Phone>', '<Phone>+777</Phone>'),
     ]
)
def test_api_create_invalid_xml(api_client, payload):
    resp = api_client.post(
        reverse('rawentity-list'),
        {
            'payload': payload
        },
        format='json'
    )
    assert resp.status_code == 201
    assert resp.data['payload'] == payload
    assert resp.data['is_valid'] is False

# TODO: if several services is_main=True?
