from django import forms
from ambiente.models import Ambiente
from usuarios.models import UsuarioAlcada


class AcessoForm(forms.Form):
    ambiente = forms.ModelChoiceField(
        queryset=Ambiente.objects.none(),
        label='Ambiente',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        usuario_id = kwargs.pop('usuario_id', None)
        super().__init__(*args, **kwargs)
        
        if usuario_id:
            # Obtém os IDs dos ambientes que o usuário tem acesso
            ambientes_ids = UsuarioAlcada.objects.filter(
                usuario_id=usuario_id
            ).values_list('ambiente_id', flat=True)
            
            # Filtra o queryset para mostrar apenas os ambientes permitidos
            self.fields['ambiente'].queryset = Ambiente.objects.filter(
                id__in=ambientes_ids
            ).order_by('nome')
