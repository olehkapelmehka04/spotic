from django.shortcuts import get_object_or_404
from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.models import Genre
from .models import Song, Playlist, SongEstimation
from .serializers import (
    SongSerializer,
    SongEstimationSerializer,
    PlaylistSerializer, GenreSerializer,
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


def recommend_response(data):
    return Response({'songs': data}, status=status.HTTP_200_OK)


class FindByGenreAPIView(APIView):
    def get(self, request):
        genre = request.GET.get('genre')
        if not genre:
            return Response({'error': 'Genre not selected'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "songs": SongSerializer(
                Song.objects.filter(genre=genre), many=True).data
        }, status=status.HTTP_200_OK)


class MyWaveAPIView(APIView):
    def get(self, request):
        user_genres = request.user.genres
        if not user_genres:
            return recommend_response('No genres')
        user_rated_song = SongEstimation.objects.filter(listener=request.user).values_list('id', flat=True)
        if not user_rated_song:
            return recommend_response(SongSerializer(Song.objects.filter(genre__in=user_genres)[:10]).data)
        candidate_songs = Song.objects.filter(genre__in=user_genres).exclude(id__in=user_rated_song)
        if not candidate_songs:
            return recommend_response(SongSerializer(Song.objects.filter(genre__in=user_genres)[:10]).data)
        liked_by_others = SongEstimation.objects.filter(id__in=candidate_songs, estimation='liked').values_list('id', flat=True)
        if not liked_by_others:
            return recommend_response(SongSerializer(candidate_songs.order_by('-release_date')[:10], many=True).data)
        recommended_songs = candidate_songs.filter(id__in=liked_by_others).order_by('-release_date')[:10]
        return recommended_songs(SongSerializer(recommended_songs, many=True).data)


class RateSongAPIView(APIView):
    def post(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        SongEstimation.objects.filter(listener=request.user, song=song).delete()
        serializer = SongEstimationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(listener=request.user, song=song)
        return Response({"estimated": serializer.data}, status=status.HTTP_201_CREATED)


class CreateGenreApiView(APIView):
    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'Incorrect data'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'genre': serializer.data}, status=status.HTTP_201_CREATED)


class GenresApiView(APIView):
    def get(self, request):
        return Response({'genres': GenreSerializer(Genre.objects.all(), many=True).data}, status=status.HTTP_200_OK)
