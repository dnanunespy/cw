# Generated by Django 5.1 on 2024-09-28 12:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0011_alter_reserva_recurso'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagemEspacoCoworking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(upload_to='fotos/')),
                ('espaco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagens', to='reservas.espacocoworking')),
            ],
        ),
    ]
