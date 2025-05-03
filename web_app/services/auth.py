from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

class AuthService:
    @staticmethod
    def register_user(request):
        """
        Registra un nuevo usuario
        Retorna: (success: bool, result: Union[User, Form], message: str)
        """
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return True, user, "Registro exitoso"
            return False, form, "Formulario inválido"
        
        return False, UserCreationForm(), "Formulario no enviado"