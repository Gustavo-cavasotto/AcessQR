# Generated by Django 5.0.6 on 2025-05-01 04:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ambiente', '0001_initial'),
        ('qrcode', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='qrcode',
            name='ambiente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='qrcodes', to='ambiente.ambiente'),
            preserve_default=False,
        ),
    ]
