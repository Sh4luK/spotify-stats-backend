from django.urls import path
from .views import SpotifyLoginView, SpotifyCallbackView, UserProfileView

urlpatterns = [
    path("auth/login/", SpotifyLoginView.as_view(), name="spotify-login"),
    path("auth/callback/", SpotifyCallbackView.as_view(), name="spotify-callback"),
    path("user/profile/", UserProfileView.as_view(), name="user-profile"),
]