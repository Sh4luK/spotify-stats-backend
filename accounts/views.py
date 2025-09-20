import os
import datetime
from django.shortcuts import redirect
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from spotify.services import exchange_code_for_token, get_user_profile

class SpotifyLoginView(APIView):
    def get(self, request):
        # ADICIONADO 'playlist-read-private' À LISTA DE SCOPES
        scopes = "user-top-read user-read-recently-played user-read-email user-library-read playlist-read-private"
        
        auth_url = (
            "https://accounts.spotify.com/authorize"
            f"?client_id={os.getenv('SPOTIFY_CLIENT_ID')}"
            f"&response_type=code"
            f"&redirect_uri={os.getenv('SPOTIFY_REDIRECT_URI')}"
            f"&scope={scopes}"
        )
        return redirect(auth_url)

class SpotifyCallbackView(APIView):
    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return Response({"error": "Code not found in request"}, status=400)

        token_data = exchange_code_for_token(code)
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        expires_in = token_data.get("expires_in")
        
        if not access_token:
            return Response({"error": "Could not get access token from Spotify"}, status=400)

        profile_data = get_user_profile(access_token)
        
        user, created = User.objects.update_or_create(
            spotify_id=profile_data["id"],
            defaults={
                "display_name": profile_data.get("display_name"),
                "email": profile_data.get("email"),
                "avatar_url": profile_data["images"][0]["url"] if profile_data.get("images") else None,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_expires_at": timezone.now() + datetime.timedelta(seconds=expires_in),
            }
        )
        
        frontend_url = os.getenv("FRONTEND_URL")
        
        return redirect(f"{frontend_url}/dashboard.html?user_id={user.spotify_id}")


class UserProfileView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "user_id is required"}, status=400)
        
        try:
            user = User.objects.get(spotify_id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)