from django import forms
from .models import Usuario, UsuarioAlcada
from ambiente.models import Ambiente


class UsuarioForm(forms.ModelForm):
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Senha',
        required=False,
        help_text='Deixe em branco para manter a senha atual'
    )

    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'senha', 'tipo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
        }

class UsuarioAlcadaForm(forms.ModelForm):
    class Meta:
        model = UsuarioAlcada
        fields = ['ambiente']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ambiente'].widget.attrs.update({'class': 'form-select'})
