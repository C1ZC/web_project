from django.db import models
from django.contrib.auth.models import User

class Pokemon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pokemons')
    pokemon_id = models.IntegerField()
    name = models.CharField(max_length=100)
    weight = models.IntegerField()
    height = models.IntegerField()
    base_experience = models.IntegerField()
    image_url = models.URLField()
    types = models.JSONField()  # Almacena los tipos como JSON
    stats = models.JSONField()  # Almacena las estadísticas como JSON
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'pokemon_id']  # Evita duplicados por usuario
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.user.username})"