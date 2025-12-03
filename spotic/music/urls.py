from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.CreateSongAPIView.as_view()),
    path("playlist/", views.CreatePlaylistAPIView.as_view()),
    path("<int:song_id>/", views.SongAPIView.as_view()),
    path("playlist/<int:playlist_id>/", views.PlaylistAPIView.as_view()),
    path("playlist/add/<int:playlist_id>/<int:song_id>/", views.AddSongPlaylist.as_view()),
]
