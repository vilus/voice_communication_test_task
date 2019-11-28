from rest_framework import serializers

from info.models import RawEntity


class RawEntitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RawEntity
        fields = '__all__'

    def validate_payload(self, value):
        # TODO: unpretty-normalize xml
        return value
