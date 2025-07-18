# Generated by Django 5.0.6 on 2025-04-30 04:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ambiente', '0001_initial'),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acesso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('autorizado', 'Autorizado'), ('negado', 'Negado')], max_length=20)),
                ('ambiente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ambiente.ambiente')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.usuario')),
            ],
            options={
                'db_table': 'acesso',
            },
        ),
    ]
