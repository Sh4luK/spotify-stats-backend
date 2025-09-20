from django.apps import AppConfig

class StatsConfig(AppConfig): # <-- Verifique este nome
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stats'