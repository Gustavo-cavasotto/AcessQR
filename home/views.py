from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime, timedelta

from ambiente.models import Ambiente
from acesso.models import Acesso
from usuarios.models import Usuario
from qrcode.models import QrCode
from django.contrib.auth.models import User

@login_required(login_url='login')
def home(request):
    usuario_logado = request.user    
    hoje = timezone.now().date()
    print(usuario_logado.id)
    # Busca o objeto Usuario correspondente ao user logado
    user_django  = User.objects.get(id=usuario_logado.id)
    usuario = Usuario.objects.get(nome=usuario_logado.username)
    

    # Estatísticas para os cards
    total_acessos = Acesso.objects.filter(
        data_hora__date=hoje
    ).count()

    total_usuarios = Usuario.objects.count()

    total_ambientes = Ambiente.objects.count()

    # QR Codes ativos
    total_qrcodes_ativos = QrCode.objects.filter(
        status='A'
    ).count()

    # Últimos acessos (diferentes para admin e usuário comum)
    if usuario.tipo == 'A':  # Administrador
        ultimos_acessos = Acesso.objects.all().order_by('-data_hora')[:10]
    else:
        ultimos_acessos = Acesso.objects.filter(
            usuario=usuario
        ).order_by('-data_hora')[:10]

    # QR Codes do usuário ou todos para admin
    if usuario.tipo == 'A':
        qrcodes = QrCode.objects.all().order_by('-validade_inicio')[:5]
    else:
        qrcodes = QrCode.objects.filter().order_by('-validade_inicio')[:5]

    # Ambientes (mantendo a funcionalidade de pesquisa existente)
    object_list = Ambiente.objects.all()
    search_value = request.GET.get('search_value')

    if search_value:
        object_list = object_list.filter(nome__icontains=search_value)

    paginator = Paginator(object_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Estatísticas adicionais para admins
    if usuario.tipo == 'A':
        acessos_semana = Acesso.objects.filter(
            data_hora__gte=timezone.now() - timedelta(days=7)
        ).count()

        usuarios_por_tipo = {
            'administradores': Usuario.objects.filter(tipo='A').count(),
            'funcionarios': Usuario.objects.filter(tipo='F').count(),
            'hospedes': Usuario.objects.filter(tipo='H').count()
        }
    else:
        acessos_semana = None
        usuarios_por_tipo = None

    context = {
        # Dados da dashboard
        'total_acessos': total_acessos,
        'total_usuarios': total_usuarios,
        'total_ambientes': total_ambientes,
        'total_qrcodes_ativos': total_qrcodes_ativos,
        'ultimos_acessos': ultimos_acessos,
        'qrcodes': qrcodes,
        'acessos_semana': acessos_semana,
        'usuarios_por_tipo': usuarios_por_tipo,
        'user_django': user_django,

        # Dados existentes
        'object_list': page_obj,
        'page_obj': page_obj,
        'search_field': search_value,
        'name': 'Dashboard',
        'operacao': 'Visão Geral do Sistema',

        # Dados do usuário
        'usuario': usuario
    }

    return render(request, 'home/templates/home.html', context)
