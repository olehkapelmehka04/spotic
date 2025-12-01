from django.db import models
from auth_app.models import CustomUser


class Song(models.Model):
    class GenreChoices(models.TextChoices):
        ROCK = ("rock", "Rock")
        POP = ("pop", "Pop")
        JAZZ = ("jazz", "Jazz")
        BLUES = ("blues", "Blues")
        HIP_HOP = ("hip-hop", "Hip-Hop")
        RAP = ("rap", "Rap")
        CLASSICAL = ("classical", "Classical")
        ELECTRONIC = ("electronic", "Electronic")
        HOUSE = ("house", "House")
        TECHNO = ("techno", "Techno")
        METAL = ("metal", "Metal")
        PUNK = ("punk", "Punk")
        COUNTRY = ("country", "Country")
        REGGAE = ("reggae", "Reggae")
        FOLK = ("folk", "Folk")
        RNB = ("r&b", "R&B")
        SOUL = ("soul", "Soul")
        DISCO = ("disco", "Disco")
        TRAP = ("trap", "Trap")
        DRUM_AND_BASS = ("drum and bass", "Drum and Bass")
        INDIE = ("indie", "Indie")
        LOFI = ("lo-fi", "Lo-fi")
        AMBIENT = ("ambient", "Ambient")
        SOUNDTRACK = ("soundtrack", "Soundtrack")

    title = models.CharField(max_length=128)
    singer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "singer"},
        related_name="songs",
    )
    duration = models.PositiveIntegerField()
    genre = models.CharField(max_length=30, choices=GenreChoices)
    release_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.singer.username}"


class SongEstimation(models.Model):
    class EstimationChoices(models.TextChoices):
        LISTENED = ("listened", "Listened")
        LIKED = ("liked", "Liked")
        DISLIKED = ("disliked", "Disliked")
        SKIPPED = ("skipped", "Skipped")

    listener = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "listener"},
        related_name="estimations",
    )
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="estimations")
    estimation = models.CharField(max_length=20, choices=EstimationChoices)

    class Meta:
        unique_together = ["listener", "song"]


class Playlist(models.Model):
    class VisibilityChoices(models.TextChoices):
        PUBLIC = ("public", "Public")
        PRIVATE = ("private", "Private")

    playlist_name = models.CharField(max_length=128)
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "listener"},
        related_name="playlists",
    )
    visibility = models.CharField(
        max_length=12, choices=VisibilityChoices, default=VisibilityChoices.PRIVATE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.playlist_name} by {self.owner.username}"


class PlaylistSong(models.Model):
    playlist = models.ForeignKey(
        Playlist, on_delete=models.CASCADE, related_name="songs"
    )
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="appearances")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["playlist", "song"]

    def __str__(self):
        return f"{self.song.title} in {self.playlist.playlist_name}"
