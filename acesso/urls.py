from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.acesso, name='verificar_acesso'),
    path('ler-qrcode/', views.ler_qrcode, name='ler_qrcode'),
    path('validar-qrcode/', views.validar_qrcode, name='validar_qrcode'),
    path('qrcode-detalhado/', views.qrcode_detalhado, name='qrcode_detalhado'),
]
