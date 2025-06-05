from django.urls import path
from . import views

urlpatterns = [
    path('acessos/', views.relatorio_acessos, name='relatorio_acessos'),
    path('acessos/pdf/', views.relatorio_acessos_pdf, name='relatorio_acessos_pdf'),
]