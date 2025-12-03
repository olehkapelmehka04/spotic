from rest_framework import serializers

from auth_app.models import CustomUser, Genre
from .models import Song, SongEstimation, Playlist, PlaylistSong


class SongSerializer(serializers.ModelSerializer):
    singer_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source="singer",
        write_only=True,
    )

    class Meta:
        model = Song
        fields = [
            "title",
            "singer_id",
            "duration",
            "genre",
            "release_date",
        ]


class SongEstimationSerializer(serializers.ModelSerializer):
    listener_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source="listener",
        write_only=True,
    )

    song_id = serializers.PrimaryKeyRelatedField(
        queryset=Song.objects.all(),
        source="song",
        write_only=True,
    )

    class Meta:
        model = SongEstimation
        fields = ["listener", "listener_id", "song", "song_id", "estimation"]


class PlaylistSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source="owner",
        write_only=True,
    )

    class Meta:
        model = Playlist
        fields = ["playlist_name", "owner_id", "visibility"]


class PlaylistSongSerializer(serializers.ModelSerializer):
    playlist_id = serializers.PrimaryKeyRelatedField(
        queryset=Playlist.objects.all(),
        source="playlist",
        write_only=True,
    )
    song_id = serializers.PrimaryKeyRelatedField(
        queryset=Song.objects.all(),
        source="song",
        write_only=True,
    )

    class Meta:
        model = PlaylistSong
        fields = ["playlist", "playlist_id", "song", "song_id"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'display_name']
