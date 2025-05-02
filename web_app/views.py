from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .services.pokemon_service import PokemonService
from .models import Pokemon
from django.db.models import Q
from django.core.paginator import Paginator

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def home(request):
    # Verificar pokémon faltantes
    missing_count, total_pokemons = PokemonService.get_missing_pokemon_count(request.user)
    has_all_pokemons = missing_count == 0
    
    if request.method == 'POST' and 'fetch_pokemons' in request.POST:
        try:
            missing_pokemons = PokemonService.fetch_missing_pokemons(request.user)
            if missing_pokemons:
                PokemonService.save_pokemons_for_user(request.user, missing_pokemons)
                messages.success(request, f'¡{len(missing_pokemons)} nuevos Pokémon guardados exitosamente!')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error al obtener los Pokémon: {str(e)}')
    
    # Obtener parámetros de filtrado y ordenamiento
    search = request.GET.get('search', '')
    order_by = request.GET.get('order_by', 'pokemon_id')
    view_type = request.GET.get('view_type', 'cards')
    
    # Filtrar y ordenar pokémon
    pokemons = Pokemon.objects.filter(user=request.user)
    if search:
        pokemons = pokemons.filter(name__icontains=search)
    
    # Aplicar ordenamiento
    order_mapping = {
        'pokemon_id': 'pokemon_id',
        'pokemon_id_desc': '-pokemon_id',
        'name': 'name',
        'name_desc': '-name',
        'weight': 'weight',
        'weight_desc': '-weight',
        'experience': 'base_experience',
        'experience_desc': '-base_experience'
    }
    pokemons = pokemons.order_by(order_mapping.get(order_by, 'pokemon_id'))
    
    # Paginación
    paginator = Paginator(pokemons, 15)  # 15 Pokémon por página
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'has_all_pokemons': has_all_pokemons,
        'missing_count': missing_count,
        'total_pokemons': total_pokemons,
        'pokemons': page_obj,  # Ahora pasamos el objeto de página
        'view_type': view_type,
        'current_order': order_by,
        'search': search
    }
    return render(request, 'pages/home.html', context)

@login_required
def pokemon_detail(request, pokemon_id):
    pokemon = Pokemon.objects.get(user=request.user, pokemon_id=pokemon_id)
    return render(request, 'components/pokemon/pokemon_detail.html', {'pokemon': pokemon})

