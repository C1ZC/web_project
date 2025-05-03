from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .services.pokemon_dashboard import PokemonDashboardService
from .services.auth import AuthService
from .services.home_service import HomeService

def register(request):
    success, result, message = AuthService.register_user(request)

    if success:
        messages.success(request, message)
        return redirect('home')

    return render(request, 'registration/register.html', {'form': result})

@login_required
def home(request):
    try:
        context, new_pokemons_count = HomeService.get_home_data(request)

        if new_pokemons_count > 0:
            messages.success(
                request,
                f'¡{new_pokemons_count} nuevos Pokémon guardados exitosamente!'
            )
            return redirect('home')

        return render(request, 'pages/home.html', context)

    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('home')


@login_required
def pokemon_detail(request, pokemon_id):
    try:
        result = HomeService.get_pokemon_detail(request.user, pokemon_id)

        if not result['success']:
            messages.error(request, result['message'])
            return redirect('home')

        return render(request, 'components/pokemon/pokemon_detail.html', result)

    except Exception as e:
        messages.error(request, f'Error al cargar el pokémon: {str(e)}')
        return redirect('home')

@login_required
def dashboard(request):
    try:
        context = PokemonDashboardService.get_dashboard_data(request.user)
        return render(request, 'pages/dashboard.html', context)
    except Exception as e:
        messages.error(request, f'Error al cargar el dashboard: {str(e)}')
        return redirect('home')
