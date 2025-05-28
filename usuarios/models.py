from django.db import models

# Create your models here.
# Tipo de usuário
class TipoUsuario(models.TextChoices):
    ADMINISTRADOR = 'A', 'Administrador'
    FUNCIONARIO = 'F', 'Funcionário'
    HOSPEDE = 'H', 'Hóspede'
    USUARIO = 'U', 'Usuário'
    
class Usuario(models.Model):
    class Meta:
        db_table = 'usuario'
        
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    senha = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TipoUsuario.choices)

    def __str__(self):
        return self.nome