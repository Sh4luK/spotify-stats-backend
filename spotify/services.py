# /backend/spotify/services.py (ATUALIZADO)

import os
import requests
from django.utils import timezone
from datetime import timedelta
from accounts.models import User

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"

def exchange_code_for_token(code):
    data = { "grant_type": "authorization_code", "code": code, "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"), "client_id": os.getenv("SPOTIFY_CLIENT_ID"), "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"), }
    response = requests.post(SPOTIFY_TOKEN_URL, data=data)
    return response.json()

def refresh_access_token(user):
    data = { "grant_type": "refresh_token", "refresh_token": user.refresh_token, "client_id": os.getenv("SPOTIFY_CLIENT_ID"), "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"), }
    response = requests.post(SPOTIFY_TOKEN_URL, data=data)
    token_data = response.json()
    user.access_token = token_data['access_token']
    user.token_expires_at = timezone.now() + timedelta(seconds=token_data['expires_in'])
    user.save(update_fields=['access_token', 'token_expires_at'])
    return user.access_token

def get_spotify_api_headers(user):
    if user.token_expires_at < timezone.now():
        access_token = refresh_access_token(user)
    else:
        access_token = user.access_token
    return {"Authorization": f"Bearer {access_token}"}

def get_user_profile(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{SPOTIFY_API_BASE_URL}/me", headers=headers)
    return response.json()

def get_user_top_items(user, item_type, period="medium_term", limit=20):
    headers = get_spotify_api_headers(user)
    params = {"time_range": period, "limit": limit}
    response = requests.get(f"{SPOTIFY_API_BASE_URL}/me/top/{item_type}", headers=headers, params=params)
    return response.json()

def get_recently_played(user, limit=50):
    headers = get_spotify_api_headers(user)
    params = {"limit": limit}
    response = requests.get(f"{SPOTIFY_API_BASE_URL}/me/player/recently-played", headers=headers, params=params)
    return response.json()

def get_audio_features(user, track_ids):
    headers = get_spotify_api_headers(user)
    params = {"ids": ",".join(track_ids)}
    response = requests.get(f"{SPOTIFY_API_BASE_URL}/audio-features", headers=headers, params=params)
    return response.json()

# --- NOVA FUNÇÃO ADICIONADA ---
def get_user_playlists(user, limit=20):
    headers = get_spotify_api_headers(user)
    params = {"limit": limit}
    response = requests.get(f"{SPOTIFY_API_BASE_URL}/me/playlists", headers=headers, params=params)
    return response.json()