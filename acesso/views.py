from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from acesso.forms import AcessoForm
from qrcode.models import QrCode, QrCodeUsuario
from ambiente.models import Ambiente
from datetime import datetime
from usuarios.models import Usuario

# Create your views here
def acesso(request):
    if request.method == 'POST':
        form = AcessoForm(request.POST)
        if form.is_valid():
            ambiente = form.cleaned_data['ambiente']
            usuario = Usuario.objects.get(id=request.session['usuario_id'])
            data_atual = datetime.now()

            # Verifica se existe um QR Code válido para o ambiente
            qrcode = QrCode.objects.filter(
                ambiente=ambiente,
                status='A',
                validade_inicio__lte=data_atual,
                validade_fim__gte=data_atual
            ).first()

            if qrcode:
                # Verifica se o usuário está na lista de usuários permitidos
                usuario_permitido = QrCodeUsuario.objects.filter(
                    qrcode=qrcode,
                    usuario=usuario
                ).exists()

                if usuario_permitido:
                    return JsonResponse({
                        'status': 'autorizado',
                        'mensagem': f'Acesso autorizado ao ambiente {ambiente.nome}',
                        'qrcode_id': qrcode.id,
                        'codigo': qrcode.codigo
                    })
                else:
                    return JsonResponse({
                        'status': 'negado',
                        'mensagem': 'Você não tem permissão para acessar este ambiente'
                    })
            else:
                return JsonResponse({
                    'status': 'negado',
                    'mensagem': 'Não há QR Code válido para este ambiente'
                })
        else:
            return JsonResponse({
                'status': 'erro',
                'mensagem': 'Dados inválidos'
            }, status=400)
    else:
        form = AcessoForm()
        return render(request, 'acesso/templates/acess.html', {'form': form})
