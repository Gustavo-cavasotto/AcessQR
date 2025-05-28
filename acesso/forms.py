from django import forms
from ambiente.models import Ambiente


class AcessoForm(forms.Form):
    ambiente = forms.ModelChoiceField(
        queryset=Ambiente.objects.all(),
        label='Ambiente',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
