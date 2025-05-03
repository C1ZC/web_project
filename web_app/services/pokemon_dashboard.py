from django.core.serializers.json import DjangoJSONEncoder
import json
from ..models import Pokemon

class PokemonDashboardService:
    @staticmethod
    def get_dashboard_data(user):
        """Obtener todos los datos necesarios para el dashboard"""
        user_pokemons = Pokemon.objects.filter(user=user)
        total_pokemons = user_pokemons.count()

        if total_pokemons == 0:
            return PokemonDashboardService._get_empty_dashboard_data()

        # Conteo de pokémon tipo Dark
        dark_count = sum(1 for pokemon in user_pokemons
                        if any(t['type']['name'].lower() == 'dark'
                             for t in pokemon.types))

        # Calcular datos de tipos
        types_count = {}
        stats_sum = [0] * 6

        for pokemon in user_pokemons:
            # Contar tipos
            for poke_type in pokemon.types:
                type_name = poke_type['type']['name'].capitalize()
                types_count[type_name] = types_count.get(type_name, 0) + 1
            
            # Sumar estadísticas
            for i, stat in enumerate(pokemon.stats):
                stats_sum[i] += stat['base_stat']

        # Top 10 por experiencia
        top_exp = user_pokemons.order_by('-base_experience')[:10]

        # Preparar datos para los gráficos
        chart_data = {
            'types': {
                'labels': list(types_count.keys()),
                'values': list(types_count.values())
            },
            'stats': [round(s / total_pokemons, 2) for s in stats_sum],
            'experience': {
                'labels': [p.name for p in top_exp],
                'values': [p.base_experience for p in top_exp]
            }
        }

        # Estadísticas generales
        stats = {
            'total': total_pokemons,
            'highest_exp': user_pokemons.order_by('-base_experience').first(),
            'lowest_hp': min(user_pokemons, key=lambda p: p.stats[0]['base_stat']),
            'dark_count': dark_count
        }

        return {
            'stats': stats,
            'chart_data': json.dumps(chart_data, cls=DjangoJSONEncoder, ensure_ascii=False)
        }

    @staticmethod
    def _get_empty_dashboard_data():
        """Retorna datos vacíos para el dashboard cuando no hay pokémon"""
        return {
            'stats': {
                'total': 0,
                'highest_exp': None,
                'lowest_hp': None,
                'dark_count': 0
            },
            'chart_data': json.dumps({
                'types': {'labels': [], 'values': []},
                'stats': [0, 0, 0, 0, 0, 0],
                'experience': {'labels': [], 'values': []}
            }, cls=DjangoJSONEncoder, ensure_ascii=False)
        }