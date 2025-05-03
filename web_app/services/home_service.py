from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from ..models import Pokemon, UserPreferences
from .pokemon_service import PokemonService

class HomeService:
    ORDER_MAPPING = {
        'pokemon_id': 'pokemon_id',
        'pokemon_id_desc': '-pokemon_id',
        'name': 'name',
        'name_desc': '-name',
        'weight': 'weight',
        'weight_desc': '-weight',
        'experience': 'base_experience',
        'experience_desc': '-base_experience'
    }

    @staticmethod
    def handle_user_preferences(request, preferences):
        """Maneja las preferencias del usuario"""
        if request.method == 'GET':
            total_pokemons = request.GET.get('total_pokemons')
            load_count = request.GET.get('load_count')
            
            if total_pokemons:
                preferences.total_pokemons = max(1, int(total_pokemons))
            if load_count:
                preferences.load_count = max(1, int(load_count))
            preferences.save()

        return preferences.total_pokemons, preferences.load_count

    @staticmethod
    def handle_pokemon_fetch(request, user, total_pokemons, load_count):
        """Maneja la obtención de nuevos pokémon"""
        if request.method == 'POST' and 'fetch_pokemons' in request.POST:
            missing_pokemons = PokemonService.fetch_missing_pokemons(
                user, total_pokemons, load_count)
            if missing_pokemons:
                PokemonService.save_pokemons_for_user(user, missing_pokemons)
                return len(missing_pokemons)
        return 0

    @staticmethod
    def get_filtered_pokemons(user, search='', order_by='pokemon_id'):
        """Obtiene los pokémon filtrados y ordenados"""
        pokemons = Pokemon.objects.filter(user=user)
        if search:
            pokemons = pokemons.filter(name__icontains=search)
        
        order_field = HomeService.ORDER_MAPPING.get(order_by, 'pokemon_id')
        return pokemons.order_by(order_field)

    @staticmethod
    def get_home_data(request):
        """Obtiene todos los datos necesarios para la vista home"""
        # Obtener o crear preferencias
        preferences, _ = UserPreferences.objects.get_or_create(user=request.user)
        
        # Manejar preferencias
        total_pokemons, load_count = HomeService.handle_user_preferences(request, preferences)

        # Verificar pokémon faltantes
        missing_count, _ = PokemonService.get_missing_pokemon_count(
            request.user, total_pokemons)
        has_all_pokemons = missing_count == 0

        # Manejar fetch de pokémon
        new_pokemons_count = HomeService.handle_pokemon_fetch(
            request, request.user, total_pokemons, load_count)

        # Obtener parámetros de filtrado
        search = request.GET.get('search', '')
        order_by = request.GET.get('order_by', 'pokemon_id')
        view_type = request.GET.get('view_type', 'cards')

        # Obtener pokémon filtrados
        pokemons = HomeService.get_filtered_pokemons(request.user, search, order_by)

        # Paginación
        paginator = Paginator(pokemons, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        return {
            'has_all_pokemons': has_all_pokemons,
            'missing_count': missing_count,
            'total_pokemons': total_pokemons,
            'load_count': load_count,
            'pokemons': page_obj,
            'view_type': view_type,
            'current_order': order_by,
            'search': search
        }, new_pokemons_count

    @staticmethod
    def get_pokemon_detail(user, pokemon_id):
        """Obtiene el detalle de un pokemon específico"""
        try:
            pokemon = get_object_or_404(Pokemon, user=user, pokemon_id=pokemon_id)
            return {
                'pokemon': pokemon,
                'success': True,
                'message': None
            }
        except Pokemon.DoesNotExist:
            return {
                'pokemon': None,
                'success': False,
                'message': 'Pokémon no encontrado'
            }