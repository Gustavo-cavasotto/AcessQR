from django.db import models

from ambiente.models import Ambiente
from usuarios.models import Usuario

class Acesso(models.Model):
    class Meta:
        db_table = 'acesso'
        
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    ambiente = models.ForeignKey(Ambiente, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)
    STATUS_ACESSO = [
        ('autorizado', 'Autorizado'),
        ('negado', 'Negado'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_ACESSO)

    def __str__(self):
        return f"{self.usuario} -> {self.ambiente} em {self.data_hora}"