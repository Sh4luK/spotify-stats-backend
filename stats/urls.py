from django.urls import path
from .views import (
    TopTracksView, 
    TopArtistsView, 
    RecentlyPlayedView, 
    AudioFeaturesView, 
    PlaylistsView,
    TopGenresView,
    TimeCapsuleView # Importa a nova view
)

urlpatterns = [
    path("user/top-tracks/", TopTracksView.as_view(), name="top-tracks"),
    path("user/top-artists/", TopArtistsView.as_view(), name="top-artists"),
    path("user/recently-played/", RecentlyPlayedView.as_view(), name="recently-played"),
    path("user/audio-features/", AudioFeaturesView.as_view(), name="audio-features"),
    path("user/playlists/", PlaylistsView.as_view(), name="playlists"),
    path("user/top-genres/", TopGenresView.as_view(), name="top-genres"),
    path("user/time-capsule/", TimeCapsuleView.as_view(), name="time-capsule"),
]