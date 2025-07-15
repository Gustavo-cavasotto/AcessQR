from django.db import models
from usuarios.models import Usuario

# Create your models here.

class LoginLog(models.Model):
    class Meta:
        db_table = 'login_log'
        
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()  # Para capturar informações do dispositivo/navegador
    TIPO_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='login')
    
    def __str__(self):
        return f"{self.usuario.nome} - {self.tipo} em {self.data_hora}"

    @property
    def dispositivo(self):
        """Extrai informações do dispositivo do user_agent"""
        if 'Mobile' in self.user_agent:
            return 'Mobile'
        elif 'Tablet' in self.user_agent:
            return 'Tablet'
        elif 'Windows' in self.user_agent:
            return 'Windows'
        elif 'Mac' in self.user_agent:
            return 'Mac'
        elif 'Linux' in self.user_agent:
            return 'Linux'
        else:
            return 'Desktop'

    @property
    def navegador(self):
        """Extrai informações do navegador do user_agent"""
        if 'Chrome' in self.user_agent:
            return 'Chrome'
        elif 'Firefox' in self.user_agent:
            return 'Firefox'
        elif 'Safari' in self.user_agent:
            return 'Safari'
        elif 'Edge' in self.user_agent:
            return 'Edge'
        else:
            return 'Outro'
