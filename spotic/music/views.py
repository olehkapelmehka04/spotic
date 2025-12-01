from django.shortcuts import get_object_or_404
from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Song, Playlist, SongEstimation
from .serializers import (
    SongSerializer,
    SongEstimationSerializer,
    PlaylistSerializer,
)


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
        user_genres = request.user.genres
        if not user_genres:
            return Response({'songs': 'No songs'}, status=status.HTTP_200_OK)
        user_rated_song_ids = SongEstimation.objects.filter(listener=request.user).values_list('id', flat=True)
        candidate_songs = Song.objects.filter(genre__in=user_genres).exclude(id__in=user_rated_song_ids)
        liked_by_others = (SongEstimation.objects.filter(song__in=candidate_songs, estimation='liked')
                           .exclude(listener=request.user)
                           .values_list('id', flat=True))
        if not liked_by_others:
            return Response({"songs": SongSerializer(candidate_songs.order_by('-release_date')[:10], many=True).data}, status=status.HTTP_200_OK)
        recommended_songs = candidate_songs.filter(id__in=liked_by_others).order_by('-release_date')[:10]
        return Response({"songs": SongSerializer(recommended_songs, many=True).data}, status=status.HTTP_200_OK)


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
