# Create your views here.
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as logout_user
from django.contrib.auth.forms import AuthenticationForm

from usuarios.models import Usuario
from .models import LoginLog

from .forms import CadastroForm, LoginForm
from django.contrib import messages

def get_client_ip(request):
    """Captura o IP do cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

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
            
            # Registra o login
            LoginLog.objects.create(
                usuario=usuario_obj,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                tipo='login'
            )
            
            auth_login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Login ou senha inválidos, tente novamente')
            return redirect('login')
        
    else:
        form = LoginForm()
    return render(request, 'login/templates/login.html', {'form': form})

def logout(request):
    # Registra o logout antes de fazer logout
    if request.user.is_authenticated:
        try:
            usuario_obj = Usuario.objects.get(nome=request.user.username)
            LoginLog.objects.create(
                usuario=usuario_obj,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                tipo='logout'
            )
        except Usuario.DoesNotExist:
            pass
    
    logout_user(request)
    return redirect('login')
