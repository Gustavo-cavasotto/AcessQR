from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.response import TemplateResponse
from .models import Ambiente
from .forms import AmbienteForm
from core.decorators import master_required

@master_required
def listar_ambientes(request):
    ambientes = Ambiente.objects.all()
    return render(request, 'ambiente/listar_ambientes.html', {'ambientes': ambientes})


@master_required
def criar_ambiente(request):
    if request.method == 'POST':
        form = AmbienteForm(request.POST)
        if form.is_valid():
            try:
                ambiente = form.save()
                messages.success(request, 'Ambiente criado com sucesso!')
                return redirect('listar_ambientes')
            except Exception as e:
                messages.error(request, f'Erro ao criar ambiente: {str(e)}')
    else:
        form = AmbienteForm()

    return render(request, 'ambiente/criar_ambiente.html', {'form': form})


@master_required
def editar_ambiente(request, id):
    ambiente = get_object_or_404(Ambiente, id=id)

    if request.method == 'POST':
        form = AmbienteForm(request.POST, instance=ambiente)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Ambiente atualizado com sucesso!')
                return redirect('listar_ambientes')
            except Exception as e:
                messages.error(
                    request, f'Erro ao atualizar ambiente: {str(e)}')
    else:
        form = AmbienteForm(instance=ambiente)

    return render(request, 'ambiente/editar_ambiente.html', {
        'form': form,
        'ambiente': ambiente
    })


@master_required
def excluir_ambiente(request, id):
    ambiente = get_object_or_404(Ambiente, id=id)

    try:
        ambiente.delete()
        messages.success(request, 'Ambiente excluído com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao excluir ambiente: {str(e)}')

    return redirect('listar_ambientes')
