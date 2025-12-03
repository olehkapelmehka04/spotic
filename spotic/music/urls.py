from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.CreateSongAPIView.as_view()),
    path("playlist/", views.CreatePlaylistAPIView.as_view()),
    path("<int:song_id>/", views.SongAPIView.as_view()),
    path("playlist/<int:playlist_id>/", views.PlaylistAPIView.as_view()),
    path("songs-by-genre/", views.FindByGenreAPIView.as_View()),
    path("rate/<int:song_id>/", views.RateSongAPIView.as_view()),
    path("my-wave/", views.MyWaveAPIView.as_view()),
]
