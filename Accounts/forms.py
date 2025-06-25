from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import UsuarioPersonalizado

class LoginFormEstilizado(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginFormEstilizado, self).__init__(*args, **kwargs)

        self.fields['username'].label = "Correo electrónico" 
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Correo electrónico',
            'type': 'email',
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña',
        })

class FormularioRegistro(UserCreationForm):
    class Meta:
        model = UsuarioPersonalizado
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'carrera',
            'carnet',
            'ciclo',
            'foto_perfil',
        ]

    def __init__(self, *args, **kwargs):
        super(FormularioRegistro, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': field.label
                })

    # Este método guarda el username con el valor del carnet
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data.get('carnet')  # generamos que el carnet del usuario sera tomado como el campo username
        if commit:
            user.save()
        return user



from django import forms
from .models import UsuarioPersonalizado

class FormularioEditarPerfil(forms.ModelForm):
    class Meta:
        model = UsuarioPersonalizado
        fields = [
            'first_name',
            'last_name',
            'email',
            'carrera',
            'carnet',
            'ciclo',
            'foto_perfil',
        ]

    def __init__(self, *args, **kwargs):
        super(FormularioEditarPerfil, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': field.label
                })