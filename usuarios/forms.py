from django import forms
from .models import Usuario


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
