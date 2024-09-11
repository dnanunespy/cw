# Generated by Django 5.1 on 2024-09-06 00:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0005_alter_reserva_hora_fim_alter_reserva_hora_inicio'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecursosEspacoCoworking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_recurso', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('quantidade', models.PositiveIntegerField()),
                ('disponivel', models.BooleanField(default=True)),
                ('espaco_coworking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recursos', to='reservas.espacocoworking')),
            ],
        ),
    ]
