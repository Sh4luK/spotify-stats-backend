# /backend/accounts/models.py (Atualizado)

from django.db import models

class User(models.Model):
    # Django agora criará um campo 'id' automaticamente como chave primária.
    
    # A única alteração foi remover 'primary_key=True' desta linha:
    spotify_id = models.CharField(max_length=100, unique=True)
    
    display_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    avatar_url = models.URLField(max_length=500, null=True, blank=True)
    access_token = models.TextField()
    refresh_token = models.TextField()
    token_expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name or self.spotify_id