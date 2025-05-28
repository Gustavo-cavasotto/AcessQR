from django.urls import path, include
from . import views  
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('', login_required(views.home), name='home'),  
    path('usuarios/', include('usuarios.urls')),
]
