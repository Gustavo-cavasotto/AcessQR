from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from acesso.forms import AcessoForm
from qrcode.models import QrCode, QrCodeUsuario
from ambiente.models import Ambiente
from datetime import datetime
from usuarios.models import Usuario
from tools.views import sql_executa
import json
from django.contrib import messages

@login_required
def acesso(request):
    if request.method == 'POST':
        form = AcessoForm(request.POST, usuario_id=request.session['usuario_id'])
        if form.is_valid():
            ambiente = form.cleaned_data['ambiente']
            usuario = Usuario.objects.get(id=request.session['usuario_id'])
            data_atual = datetime.now()

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
                    inserir_acesso(data_atual, 'A', ambiente.id, usuario.id)
                    
                    # Dados para retorno JSON
                    response_data = {
                        'status': 'autorizado',
                        'mensagem': f'Acesso autorizado ao ambiente {ambiente.nome}',
                        'qrcode_id': str(qrcode.codigo),
                        'codigo': str(qrcode.codigo),
                        'ambiente': {
                            'nome': ambiente.nome,
                            'localizacao': ambiente.localizacao,
                        },
                        'validade': {
                            'inicio': qrcode.validade_inicio.strftime('%d/%m/%Y %H:%M'),
                            'fim': qrcode.validade_fim.strftime('%d/%m/%Y %H:%M'),
                            'inicio_iso': qrcode.validade_inicio.isoformat(),
                            'fim_iso': qrcode.validade_fim.isoformat(),
                        },
                        'usuario': usuario.nome,
                        'data_autorizacao': data_atual.strftime('%d/%m/%Y %H:%M:%S')
                    }
                    
                    # Salva na sessão para uso no template detalhado
                    request.session['qrcode_data'] = response_data
                    
                    return JsonResponse(response_data)
                else:
                    inserir_acesso(data_atual, 'N', ambiente.id, usuario.id)
                    return JsonResponse({
                        'status': 'negado',
                        'mensagem': 'Você não tem permissão para acessar este ambiente'
                    })
            else:
                inserir_acesso(data_atual, 'N', ambiente.id, usuario.id)
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
        form = AcessoForm(usuario_id=request.session['usuario_id'])
        return render(request, 'acesso/templates/acess.html', {'form': form})

def inserir_acesso(data_hora, status, ambiente, usuario):
    # Verifica se o ambiente existe
    try:
        sql = """
            INSERT INTO acesso (data_hora, status, ambiente_id, usuario_id)
            VALUES (%s, %s, %s, %s)
        """
        sql_executa(sql, [data_hora, status, ambiente, usuario])     
    except Exception as e:
        print(f"Erro ao inserir acesso: {e}")

@login_required
def validar_qrcode(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            codigo = data.get('codigo')
            print('codigo', codigo)
            
            if not codigo:
                return JsonResponse({
                    'status': 'erro',
                    'mensagem': 'Código do QR Code não fornecido'
                }, status=400)

            # Converte o código para inteiro se for string
            try:
                codigo_int = int(codigo)
            except (ValueError, TypeError):
                return JsonResponse({
                    'status': 'negado',
                    'mensagem': 'Código do QR Code inválido'
                })

            usuario = Usuario.objects.get(id=request.session['usuario_id'])
            data_atual = datetime.now()

            # Busca o QR Code pelo código
            qrcode = QrCode.objects.filter(
                codigo=codigo_int,
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
                    inserir_acesso(data_atual, 'A', qrcode.ambiente.id, usuario.id)
                    return JsonResponse({
                        'status': 'autorizado',
                        'mensagem': f'Acesso autorizado ao ambiente {qrcode.ambiente.nome}',
                        'ambiente': qrcode.ambiente.nome,
                        'data_hora': data_atual.strftime('%d/%m/%Y %H:%M:%S'),
                        'usuario': usuario.nome
                    })
                else:
                    inserir_acesso(data_atual, 'N', qrcode.ambiente.id, usuario.id)
                    return JsonResponse({
                        'status': 'negado',
                        'mensagem': 'Você não tem permissão para acessar este ambiente',
                        'ambiente': qrcode.ambiente.nome,
                        'data_hora': data_atual.strftime('%d/%m/%Y %H:%M:%S'),
                        'usuario': usuario.nome
                    })
            else:
                return JsonResponse({
                    'status': 'negado',
                    'mensagem': 'QR Code inválido ou expirado',
                    'data_hora': data_atual.strftime('%d/%m/%Y %H:%M:%S'),
                    'usuario': usuario.nome
                })
        except Exception as e:
            return JsonResponse({
                'status': 'erro',
                'mensagem': f'Erro ao processar a requisição: {str(e)}'
            }, status=500)
    else:
        return JsonResponse({
            'status': 'erro',
            'mensagem': 'Método não permitido'
        }, status=405)

@login_required
def ler_qrcode(request):
    return render(request, 'acesso/templates/ler_qrcode.html')

@login_required
def qrcode_detalhado(request):
    """Renderiza página detalhada do QR Code com informações completas"""
    if request.method == 'GET':
        # Recupera dados da sessão ou parâmetros
        qrcode_data = request.session.get('qrcode_data')
        
        if not qrcode_data:
            messages.error(request, 'Nenhum QR Code válido encontrado. Gere um novo acesso.')
            return redirect('verificar_acesso')
        
        return render(request, 'qrcode_detalhado.html', qrcode_data)
    
    return redirect('verificar_acesso')


