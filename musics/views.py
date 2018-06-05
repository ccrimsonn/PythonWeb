from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import permission_classes

from musics.models import Music
from musics.serializers import MusicSerializer

# 按照class设定权限
# class MusicViewSet(viewsets.ModelViewSet):
#     queryset = Music.objects.all()
#     serializer_class = MusicSerializer
#     permission_classes = (IsAuthenticated,)

class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer

    def get_permissions(self):
        if self.action in ('create', 'destroy',):
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    # [GET] api/musics/
    def list(self, request, **kwargs):
        songs = Music.objects.all()
        serializer = MusicSerializer(songs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # [POST] api/musics/
    @permission_classes((IsAuthenticated,))
    def create(self, request, **kwargs):
        song = request.data.get('song')
        singer = request.data.get('singer')
        songs = Music.objects.create(song=song, singer=singer)
        serializer = MusicSerializer(songs)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # [Delete] api/musics/
    @permission_classes((IsAuthenticated,))
    def destroy(self, request, *args, **kwargs):
        song_id = Music.objects.get(id=kwargs.get('pk'))
        self.perform_destroy(song_id)
        message = "Delete successful"
        return Response(message, status=status.HTTP_204_NO_CONTENT)