from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

from .models import Channel, ChannelPrice
from .serializer import ChannelPriceSerializer, ChannelSerializer


class ChannelDetail(APIView):

    def get(self, request, pk, *args, **kwargs):
        snippets = Channel.objects.all()
        serializer = ChannelSerializer(snippets, many=True)

        return Response(serializer.data)


class ChannelPriceDetail(APIView):

    def get(self, request, *args, **kwargs):
        snippets = ChannelPrice.objects.all()
        serializer = ChannelPriceSerializer(snippets, many=True)

        return Response(serializer.data)
