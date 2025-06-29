from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.response import TemplateResponse
from .models import QrCode, QrCodeUsuario
from .forms import QrCodeForm
from usuarios.models import Usuario


@login_required
def listar_qrcodes(request):
    qrcodes = QrCode.objects.all()
    return TemplateResponse(request, 'qrcode/listar_qrcodes.html', {'qrcodes': qrcodes})


@login_required
def criar_qrcode(request):
    if request.method == 'POST':
        form = QrCodeForm(request.POST)
        if form.is_valid():
            try:
                qrcode = form.save(commit=False)
                # Converte o User do Django para nosso modelo Usuario
                usuario = Usuario.objects.get(id=request.session['usuario_id'])
                qrcode.criado_por = usuario
                # Salva o QR Code e os usuários permitidos
                form.save()
                messages.success(request, 'QR Code criado com sucesso!')
                return redirect('listar_qrcodes')
            except Exception as e:
                messages.error(request, f'Erro ao criar QR Code: {str(e)}')
    else:
        form = QrCodeForm()

    return TemplateResponse(request, 'qrcode/criar_qrcode.html', {'form': form})


@login_required
def editar_qrcode(request, id):
    qrcode = get_object_or_404(QrCode, codigo=id)

    if request.method == 'POST':
        form = QrCodeForm(request.POST, instance=qrcode)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'QR Code atualizado com sucesso!')
                return redirect('listar_qrcodes')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar QR Code: {str(e)}')
    else:
        form = QrCodeForm(instance=qrcode)

    return TemplateResponse(request, 'qrcode/editar_qrcode.html', {
        'form': form,
        'qrcode': qrcode
    })


@login_required
def excluir_qrcode(request, id):
    qrcode = get_object_or_404(QrCode, codigo=id)

    try:
        qrcode.delete()
        messages.success(request, 'QR Code excluído com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao excluir QR Code: {str(e)}')

    return redirect('listar_qrcodes')
