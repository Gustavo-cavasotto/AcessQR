# Create your views here.
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as logout_user
from django.contrib.auth.forms import AuthenticationForm

from usuarios.models import Usuario

from .forms import CadastroForm, LoginForm
from django.contrib import messages

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro efetuado com sucesso!')
            return redirect('login')
    else:
        form = CadastroForm()
    return render(request, 'login/templates/cadastro.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            usuario_obj = Usuario.objects.get(nome=user.username)
            request.session['usuario_nome'] = usuario_obj.nome
            request.session['usuario_id'] = usuario_obj.id
            request.session['usuario_tipo'] = usuario_obj.tipo
            
            auth_login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Login ou senha inválidos, tente novamente')
            return redirect('login')
        
    else:
        form = LoginForm()
    return render(request, 'login/templates/login.html', {'form': form})


def logout(request):
    logout_user(request)
    return redirect('login')
