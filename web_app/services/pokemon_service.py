import requests
from typing import List, Dict, Tuple
from django.db.models import Count
from ..models import Pokemon

class PokemonService:
    BASE_URL = "https://pokeapi.co/api/v2"
    TOTAL_POKEMONS = 151  # Total de pokémon que queremos
    
    @staticmethod
    def fetch_pokemons(limit: int = 151) -> List[Dict]:
        """Obtiene los primeros N pokémon de la API"""
        response = requests.get(f"{PokemonService.BASE_URL}/pokemon?limit={limit}")
        pokemons = response.json()['results']
        
        detailed_pokemons = []
        for pokemon in pokemons:
            detail = requests.get(pokemon['url']).json()
            detailed_pokemons.append({
                'pokemon_id': detail['id'],
                'name': detail['name'],
                'weight': detail['weight'],
                'height': detail['height'],
                'base_experience': detail['base_experience'],
                'image_url': detail['sprites']['other']['official-artwork']['front_default'],
                'types': detail['types'],
                'stats': detail['stats']
            })
        return detailed_pokemons
    
    @staticmethod
    def save_pokemons_for_user(user, pokemons: List[Dict]) -> None:
        """Guarda los pokémon para un usuario específico"""
        for pokemon_data in pokemons:
            Pokemon.objects.get_or_create(
                user=user,
                pokemon_id=pokemon_data['pokemon_id'],
                defaults={
                    'name': pokemon_data['name'],
                    'weight': pokemon_data['weight'],
                    'height': pokemon_data['height'],
                    'base_experience': pokemon_data['base_experience'],
                    'image_url': pokemon_data['image_url'],
                    'types': pokemon_data['types'],
                    'stats': pokemon_data['stats']
                }
            )
    
    @staticmethod
    def get_missing_pokemon_count(user, total_pokemons) -> Tuple[int, int]:
        """
        Retorna la cantidad de pokémon faltantes y el total deseado
        """
        current_count = Pokemon.objects.filter(user=user).count()
        missing = total_pokemons - current_count
        return missing, total_pokemons

    @staticmethod
    def fetch_missing_pokemons(user, total_pokemons, load_count) -> List[Dict]:
        """
        Obtiene solo los pokémon que faltan para el usuario
        """
        existing_ids = set(Pokemon.objects.filter(user=user).values_list('pokemon_id', flat=True))
        all_pokemons = PokemonService.fetch_pokemons(total_pokemons)
        missing_pokemons = [
            p for p in all_pokemons if p['pokemon_id'] not in existing_ids]
        return missing_pokemons[:load_count]
