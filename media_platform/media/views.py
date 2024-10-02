import json
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Channel, Content, Group
from .serializers import ChannelSerializer, ContentSerializer, GroupSerializer
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class ContentListView(generics.ListAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    def list(self, request, *args, **kwargs):
        response_status = status.HTTP_200_OK
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if not serializer.data:
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ContentDetailView(generics.ListAPIView):
    query_set = Content.objects.all()
    serializer_class = ContentSerializer

class ChannelListView(generics.ListAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['groups__id', 'groups__name']

    # def list(self, request, *args, **kwargs):
    #     response_status = status.HTTP_200_OK
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)

    #     if not serializer.data:
    #         return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

class ChannelDetailView(generics.RetrieveAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

class GroupListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupDetailView(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer