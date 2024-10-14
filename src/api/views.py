from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Channel
from .serializers import ChannelSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/channels',
        'GET /api/channels/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def getChannels(request):
    channels = Channel.objects.all()
    serializer = ChannelSerializer(channels, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getChannel(request, pk):
    channel = Channel.objects.get(id=pk)
    serializer = ChannelSerializer(channel, many=False)
    return Response(serializer.data)