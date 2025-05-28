from django import forms
from .models import QrCode, QrCodeUsuario
from usuarios.models import Usuario
from ambiente.models import Ambiente


class QrCodeForm(forms.ModelForm):
    usuarios_permitidos = forms.ModelMultipleChoiceField(
        queryset=Usuario.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select select2',
            'data-placeholder': 'Selecione os usuários...',
            'data-allow-clear': 'true',
            'data-width': '100%',
            'data-tags': 'true',
            'data-token-separators': '[",", " "]'
        }),
        required=True,
        label='Usuários Permitidos',
        help_text='Digite para buscar e selecionar os usuários'
    )

    class Meta:
        model = QrCode
        fields = ['codigo', 'validade_inicio',
                  'validade_fim', 'status', 'ambiente']
        widgets = {
            'validade_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'validade_fim': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'ambiente': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['usuarios_permitidos'].initial = self.instance.usuarios_permitidos.values_list(
                'usuario', flat=True)

    def save(self, commit=True):
        qrcode = super().save(commit=False)
        if commit:
            qrcode.save()
            # Limpa os usuários existentes
            QrCodeUsuario.objects.filter(qrcode=qrcode).delete()
            # Adiciona os novos usuários
            for usuario in self.cleaned_data['usuarios_permitidos']:
                QrCodeUsuario.objects.create(qrcode=qrcode, usuario=usuario)
        return qrcode
