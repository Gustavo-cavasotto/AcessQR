from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.listar_qrcodes), name='listar_qrcodes'),
    path('criar/', login_required(views.criar_qrcode), name='criar_qrcode'),
    path('editar/<int:id>/', login_required(views.editar_qrcode), name='editar_qrcode'),
    path('excluir/<int:id>/', login_required(views.excluir_qrcode), name='excluir_qrcode'),
] 