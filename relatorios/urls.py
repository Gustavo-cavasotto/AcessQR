from django.urls import path
from . import views

urlpatterns = [
    path('acessos/', views.relatorio_acessos, name='relatorio_acessos'),
    path('acessos/pdf/', views.relatorio_acessos_pdf, name='relatorio_acessos_pdf'),
    path('acessos/nova-guia/', views.relatorio_acessos_nova_guia, name='relatorio_acessos_nova_guia'),
    path('logins/', views.relatorio_logins, name='relatorio_logins'),
    path('logins/pdf/', views.relatorio_logins_pdf, name='relatorio_logins_pdf'),
    path('logins/nova-guia/', views.relatorio_logins_nova_guia, name='relatorio_logins_nova_guia'),
]