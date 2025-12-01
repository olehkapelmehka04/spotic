from django.shortcuts import render
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
from .models import Song, Playlist, SongEstimation


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


class FindByGenre(APIView):
    def get(self, request):
        genre = request.GET.get("genre")
        if not genre:
            return Response({"error": "No genre"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"songs": SongSerializer(Song.objects.filter(genre=genre), many=True).data},
            status=status.HTTP_200_OK,
        )


class MyWave(APIView):
    def get(self, request):
        pass


class RateSong(APIView):
    def post(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        SongEstimation.objects.filter(listener=request.user, song=song).delete()
        serializer = SongEstimationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(listener=request.user, song=song)
        return Response({"estimated": serializer.data}, status=status.HTTP_201_CREATED)
