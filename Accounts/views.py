from django.contrib.auth.views import LoginView
from .forms import LoginFormEstilizado
from django.contrib import messages
from .forms import FormularioRegistro
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UsuarioPersonalizado
from .forms import FormularioEditarPerfil
from .forms import LoginFormEstilizado, FormularioRegistro, FormularioEditarPerfil



class LoginPersonalizado(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginFormEstilizado

def registro_usuario(request):
    if request.method == 'POST':
        form = FormularioRegistro(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save()
            usuario.backend = 'Accounts.backends.EmailAuthBackend' 
            login(request, usuario) #lo logueamos de una sola vez
            messages.success(request, "¡Registro exitoso!")
            return redirect('documentacion_metodos')  # Redirige a la vista de documentacion
    else:
        form = FormularioRegistro()

    return render(request, "accounts/registro.html", {"form": form})



@login_required
def editar_perfil(request):
    usuario = request.user

    if request.method == "POST":
        form = FormularioEditarPerfil(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('ver_perfil')
        else:
            print("Errores:", form.errors)
    else:
        form = FormularioEditarPerfil(instance=usuario)

    return render(request, 'accounts/editar_perfil.html', {
        'form': form,
        'usuario': usuario 
    })

@login_required
def ver_perfil(request):
    return render(request, 'accounts/perfil.html', {'usuario': request.user})