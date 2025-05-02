from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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


class UserPreferences(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='preferences')
    total_pokemons = models.IntegerField(default=151)  # Valor predeterminado
    load_count = models.IntegerField(default=10)  # Valor predeterminado

    def __str__(self):
        return f"Preferencias de {self.user.username}"


@receiver(post_save, sender=User)
def create_user_preferences(sender, instance, created, **kwargs):
    if created:
        UserPreferences.objects.create(user=instance)
