Тестовое задание для Voice Communication
=========================================

requirements:
  - linux (used bash, can be changed)
  - docker
  - docker-compose

install:



testing:

  ::

    python scripts/entity_generator.py -v -c 10

    python scripts/phones_processing.py -v -i 10 -p 2

    python manage.py shell
    from info.models import RawEntity, Entity, Phone
    r = RawEntity.objects.create(payload='xml')
    e = Entity.objects.create(name='e', raw_entity=r)
    # [Phone.objects.create(phone='+74111111111', entity=e) for _ in range(100000)]  # phones creator
    # after scripts processed phones
    Phone.objects.filter(is_mobile=None)
    Phone.objects.all().delete()

