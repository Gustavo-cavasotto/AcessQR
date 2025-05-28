from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Usuario, TipoUsuario
from django.contrib.auth.hashers import make_password
from .forms import UsuarioForm
from django.shortcuts import render
from core.decorators import master_required

@master_required
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/listar_usuarios.html', {'usuarios': usuarios})

@master_required
def criar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                usuario = form.save(commit=False)

                usuario_tipo = form.cleaned_data['tipo']
                if usuario_tipo == 'A':
                    is_superuser = True
                else:
                    is_superuser = False

                # Criar User do Django
                user = User.objects.create_user(
                    username=usuario.nome,
                    email=usuario.email,
                    password=usuario.senha,
                    first_name=usuario.nome,
                    is_superuser=is_superuser
                )

                usuario.senha = make_password(usuario.senha)
                usuario.save()

                messages.success(request, 'Usuário criado com sucesso!')
                return redirect('listar_usuarios')
            except Exception as e:
                messages.error(request, f'Erro ao criar usuário: {str(e)}')
    else:
        form = UsuarioForm()

    return render(request, 'usuarios/criar_usuario.html', {'form': form})


@master_required
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    user = User.objects.get(username=usuario.nome)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            try:
                usuario = form.save(commit=False)
                # Atualizar User do Django
                user.first_name = usuario.nome
                user.email = usuario.email
                user.username = usuario.nome
                if usuario.senha:
                    user.set_password(usuario.senha)
                    usuario.senha = make_password(usuario.senha)
                user.save()
                usuario.save()

                messages.success(request, 'Usuário atualizado com sucesso!')
                return redirect('listar_usuarios')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar usuário: {str(e)}')
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'usuarios/editar_usuario.html', {
        'form': form,
        'usuario': usuario
    })


@master_required
def excluir_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    user = User.objects.get(email=usuario.email)

    try:
        # Excluir User do Django
        user.delete()
        # Excluir Usuario do sistema
        usuario.delete()
        messages.success(request, 'Usuário excluído com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao excluir usuário: {str(e)}')

    return redirect('listar_usuarios')
