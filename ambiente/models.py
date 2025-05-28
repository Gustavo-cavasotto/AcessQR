from django.db import models

# Create your models here.
class Ambiente(models.Model):
    class Meta:
        db_table = 'ambiente'
        
    nome = models.CharField(max_length=100)
    localizacao = models.CharField(max_length=255)
    

    def __str__(self):
        return self.nome