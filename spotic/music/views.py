from re import A
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status, exceptions
from rest_framework.response import Response


from .serializers import (
    SongSerializer,
    SongEstimationSerializer,
    PlaylistSerializer,
    PlaylistSongSerializer,
)
from .models import Song, Playlist


class CreateSongAPIView(APIView):
    def post(self, request):
        data = request.data.copy()
        data["singer_id"] = request.user.id
        serializer = SongSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreatePlaylistAPIView(APIView):
    def post(self, request):
        data = request.data.copy()
        data["owner_id"] = request.user.id
        serializer = PlaylistSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SongAPIView(APIView):
    def get(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        return Response(SongSerializer(song).data)


class PlaylistAPIView(APIView):
    def get(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, id=playlist_id)
        if playlist.visibility == "private":
            if playlist.owner != request.user:
                raise exceptions.PermissionDenied("У вас нет доступа к этому плейлисту")
        return Response(PlaylistSerializer(playlist).data)
