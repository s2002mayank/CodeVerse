from rest_framework.serializers import ModelSerializer
from base.models import Channel


class ChannelSerializer(ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'