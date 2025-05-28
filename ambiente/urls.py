from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('', login_required(views.listar_ambientes), name='listar_ambientes'),
    path('criar/', login_required(views.criar_ambiente), name='criar_ambiente'),
    path('editar/<int:id>/', login_required(views.editar_ambiente), name='editar_ambiente'),
    path('excluir/<int:id>/', login_required(views.excluir_ambiente), name='excluir_ambiente'),
]
