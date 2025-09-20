from django.db import models

class TopTrack(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    spotify_track_id = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    artists = models.TextField() # Armazenado como JSON string ou texto simples
    album_cover_url = models.URLField(max_length=500, null=True)
    popularity = models.IntegerField(default=0)
    rank = models.IntegerField()
    period = models.CharField(max_length=20)  # short_term / medium_term / long_term
    fetched_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'spotify_track_id', 'period', 'rank')

# Você pode adicionar outros modelos como TopArtist aqui, seguindo a mesma lógica.