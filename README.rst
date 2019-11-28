Тестовое задание для Voice Communication
=========================================

requirements:
  - linux (used bash, can be changed)
  - docker
  - docker-compose

install:

  ::

    git clone https://github.com/vilus/voice_communication_test_task.git
    cd voice_communication_test_task
    . .bash_alias
    dcb
    dcu
    # dcd  # delete all


testing:

  ::

    # open new terminal (1)
    cd voice_communication_test_task  # to cloned repo
    . .bash_alias
    dcrb
    python scripts/phones_processing.py -v -i 10 -p 2  # could be exceptions in output, its normal, expected


    # open new terminal (2)
    cd voice_communication_test_task  # to cloned repo
    . .bash_alias
    dcrb
    python scripts/phones_processing.py -v -i 10 -p 2 # could be exceptions in output, its normal, expected


    # open new terminal (3)
    cd voice_communication_test_task  # to cloned repo
    . .bash_alias
    dcrb
    python scripts/entity_generator.py -v -c 2000  # could take long time


    # open new terminal (4)
    cd voice_communication_test_task  # to cloned repo
    . .bash_alias
    dcrb
    python manage.py shell
    from info.models import RawEntity, Entity, Phone
    # r = RawEntity.objects.create(payload='xml')
    # e = Entity.objects.create(name='e', raw_entity=r)
    # [Phone.objects.create(phone='+74111111111', entity=e) for _ in range(100000)]  # phones creator
    # after scripts processed phones
    Phone.objects.filter(is_mobile=None)
    Phone.objects.all().delete()

