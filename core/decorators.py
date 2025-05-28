from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def master_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if not request.user.is_superuser:
            messages.error(request, 'Você não tem permissão para acessar esta página.')
            return redirect('home')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view 