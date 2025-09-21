from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import User
from spotify.services import get_user_top_items, get_recently_played, get_audio_features, get_user_playlists
import statistics
from collections import Counter

class TopTracksView(APIView):
    def get(self, request):
        # --- LINHA DE TESTE ADICIONADA AQUI ---
        print("--- EXECUTANDO TopTracksView: VERSÃO MAIS RECENTE DO CÓDIGO ---")
        
        user_id = request.query_params.get('user_id')
        period = request.query_params.get('period', 'medium_term')
        if not user_id: return Response({"error": "user_id is required"}, status=400)
        try:
            user = User.objects.get(spotify_id=user_id)
            data = get_user_top_items(user, 'tracks', period=period, limit=20)
            return Response(data)
        except User.DoesNotExist: return Response({"error": "User not found"}, status=404)

class TopArtistsView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        period = request.query_params.get('period', 'medium_term')
        
        if not user_id:
            return Response({"error": "user_id is required"}, status=400)
            
        try:
            user = User.objects.get(spotify_id=user_id)
            data = get_user_top_items(user, 'artists', period=period, limit=20)
            return Response(data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class RecentlyPlayedView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id: return Response({"error": "user_id is required"}, status=400)
        try:
            user = User.objects.get(spotify_id=user_id)
            data = get_recently_played(user)
            
            total_duration_ms = 0
            if data and 'items' in data:
                for item in data['items']:
                    if 'track' in item and 'duration_ms' in item['track']:
                        total_duration_ms += item['track']['duration_ms']
            
            data['total_duration_ms'] = total_duration_ms
            
            return Response(data)
        except User.DoesNotExist: return Response({"error": "User not found"}, status=44)


class AudioFeaturesView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id: return Response({"error": "user_id is required"}, status=400)
        try:
            user = User.objects.get(spotify_id=user_id)
            top_tracks_data = get_user_top_items(user, 'tracks', limit=50)
            
            if not top_tracks_data.get('items'):
                return Response({})

            track_ids = [track['id'] for track in top_tracks_data['items']]
            features_data = get_audio_features(user, track_ids)
            
            features_list = [f for f in features_data.get('audio_features', []) if isinstance(f, dict)]

            if not features_list:
                return Response({})

            def safe_mean(data):
                valid_data = [x for x in data if x is not None]
                return statistics.mean(valid_data) if valid_data else 0.0

            average_features = {
                "danceability": safe_mean([f.get('danceability') for f in features_list]),
                "energy": safe_mean([f.get('energy') for f in features_list]),
                "valence": safe_mean([f.get('valence') for f in features_list]),
                "acousticness": safe_mean([f.get('acousticness') for f in features_list]),
                "instrumentalness": safe_mean([f.get('instrumentalness') for f in features_list]),
                "liveness": safe_mean([f.get('liveness') for f in features_list]),
            }
            return Response(average_features)
        except User.DoesNotExist: return Response({"error": "User not found"}, status=404)
        except Exception as e:
            print(f"Erro inesperado na AudioFeaturesView: {e}")
            return Response({"error": "Ocorreu um erro interno no servidor."}, status=500)

class PlaylistsView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id: return Response({"error": "user_id is required"}, status=400)
        try:
            user = User.objects.get(spotify_id=user_id)
            data = get_user_playlists(user)
            return Response(data)
        except User.DoesNotExist: return Response({"error": "User not found"}, status=404)
        
class TopGenresView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id: return Response({"error": "user_id is required"}, status=400)
        try:
            user = User.objects.get(spotify_id=user_id)
            
            top_artists_data = get_user_top_items(user, 'artists', limit=50)

            if not top_artists_data.get('items'):
                return Response({})

            all_genres = []
            for artist in top_artists_data['items']:
                all_genres.extend(artist.get('genres', []))
            
            if not all_genres:
                return Response({})

            genre_counts = Counter(all_genres)
            
            top_5_genres = genre_counts.most_common(5)
            
            processed_genres = dict(top_5_genres)
            
            others_count = sum(genre_counts.values()) - sum(processed_genres.values())
            if others_count > 0:
                processed_genres['Outros'] = others_count
                
            return Response(processed_genres)

        except User.DoesNotExist: return Response({"error": "User not found"}, status=404)

class TimeCapsuleView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id: return Response({"error": "user_id is required"}, status=400)
        try:
            user = User.objects.get(spotify_id=user_id)
            
            # Busca os dados para os três períodos
            short_term_data = get_user_top_items(user, 'artists', period='short_term', limit=50)
            medium_term_data = get_user_top_items(user, 'artists', period='medium_term', limit=50)
            long_term_data = get_user_top_items(user, 'artists', period='long_term', limit=50)

            response_data = {
                "short_term": short_term_data.get('items', []),
                "medium_term": medium_term_data.get('items', []),
                "long_term": long_term_data.get('items', []),
            }
            
            return Response(response_data)

        except User.DoesNotExist: return Response({"error": "User not found"}, status=404)