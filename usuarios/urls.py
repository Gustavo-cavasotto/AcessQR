from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.listar_usuarios), name='listar_usuarios'),
    path('criar/', login_required(views.criar_usuario), name='criar_usuario'),
    path('editar/<int:id>/', login_required(views.editar_usuario), name='editar_usuario'),
    path('excluir/<int:id>/', login_required(views.excluir_usuario), name='excluir_usuario'),
    path('alcada/<int:id>/', login_required(views.gerenciar_alcada), name='gerenciar_alcada'),
    path('alcada/<int:id>/excluir/<int:alcada_id>/', login_required(views.excluir_alcada), name='excluir_alcada'),
]
