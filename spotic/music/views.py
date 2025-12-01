from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from music.serializers import SongSerializer, SongEstimationSerializer
from .models import Song, SongEstimation


class FindByGenre(APIView):
    def get(self, request):
        genre = request.GET.get('genre')
        if not genre:
            return Response({'error': 'No genre'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'songs': SongSerializer(Song.objects.filter(genre=genre), many=True).data}, status=status.HTTP_200_OK)


class MyWave(APIView):
    def get(self, request):
        pass



class RateSong(APIView):
    def post(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        SongEstimation.objects.filter(listener=request.user,song=song).delete()
        serializer = SongEstimationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(listener=request.user, song=song)
        return Response({'estimated': serializer.data}, status=status.HTTP_201_CREATED)
