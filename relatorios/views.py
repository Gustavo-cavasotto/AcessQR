from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from acesso.models import Acesso
from usuarios.models import Usuario
from ambiente.models import Ambiente
from django.db.models import Q
from datetime import datetime
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
import io

# Create your views here.

@login_required
def relatorio_acessos(request):
    acessos = Acesso.objects.all()
    # Filtros
    usuario_id = request.GET.get('usuario')
    ambiente_id = request.GET.get('ambiente')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    status = request.GET.get('status')
    print('status', status)
    
    if usuario_id:
        acessos = acessos.filter(usuario_id=usuario_id)
    if ambiente_id:
        acessos = acessos.filter(ambiente_id=ambiente_id)
    if data_inicio:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        acessos = acessos.filter(data_hora__gte=data_inicio)
    if data_fim:
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
        acessos = acessos.filter(data_hora__lte=data_fim)
    if status:
        if status == 'autorizado':
            acessos = acessos.filter(status='A')
        elif status == 'negado':
            acessos = acessos.filter(status='N')
        else:
            acessos = acessos.filter(status=status)
    
    usuarios = Usuario.objects.all()
    ambientes = Ambiente.objects.all()
    
    context = {
        'acessos': acessos,
        'usuarios': usuarios,
        'ambientes': ambientes,
        'status_choices': Acesso.STATUS_ACESSO,
    }
    
    return render(request, 'relatorios/relatorio_acessos.html', context)

@login_required
def relatorio_acessos_pdf(request):
    acessos = Acesso.objects.all()
    
    # Filtros
    usuario_id = request.GET.get('usuario')
    ambiente_id = request.GET.get('ambiente')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    status = request.GET.get('status')
    print('status', status)
    
    if usuario_id:
        acessos = acessos.filter(usuario_id=usuario_id)
    if ambiente_id:
        acessos = acessos.filter(ambiente_id=ambiente_id)
    if data_inicio:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        acessos = acessos.filter(data_hora__gte=data_inicio)
    if data_fim:
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
        acessos = acessos.filter(data_hora__lte=data_fim)
    if status:
        if status == 'autorizado':
            acessos = acessos.filter(status='A')
        elif status == 'negado':
            acessos = acessos.filter(status='N')
        else:
            acessos = acessos.filter(status=status)
    
    context = {
        'acessos': acessos,
        'data_geracao': datetime.now().strftime('%d/%m/%Y %H:%M'),
    }
    
    # Renderiza o template HTML
    html_string = render_to_string('relatorios/relatorio_acessos_pdf.html', context)
    
    # Cria o PDF
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.StringIO(html_string), result)
    
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_acessos.pdf"'
        return response
    
    return HttpResponse('Erro ao gerar PDF', status=500)
