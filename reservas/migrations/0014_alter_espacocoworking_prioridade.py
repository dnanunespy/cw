# Generated by Django 5.1 on 2024-09-28 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0013_remove_espacocoworking_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='espacocoworking',
            name='prioridade',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
