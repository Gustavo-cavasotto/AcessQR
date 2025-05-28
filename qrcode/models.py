from django.db import models

from usuarios.models import Usuario
from ambiente.models import Ambiente
# Create your models here.


class QrCode(models.Model):
    class Meta:
        db_table = 'qrcode'

    codigo = models.CharField(max_length=255, unique=True)
    validade_inicio = models.DateTimeField()
    validade_fim = models.DateTimeField()
    STATUS_CHOICES = [
        ('A', 'Ativo'),
        ('E', 'Expirado'),
        ('R', 'Revogado'),
    ]
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='A')
    ambiente = models.ForeignKey(
        Ambiente, on_delete=models.CASCADE, related_name='qrcodes')
    criado_por = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='qrcodes_criados')

    def __str__(self):
        return self.codigo


class QrCodeUsuario(models.Model):
    class Meta:
        db_table = 'qrcode_usuarios'
        unique_together = ('qrcode', 'usuario')

    qrcode = models.ForeignKey(
        QrCode, on_delete=models.CASCADE, related_name='usuarios_permitidos')
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='qrcodes_permitidos')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.qrcode}"
