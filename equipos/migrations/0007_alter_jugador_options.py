# Generated by Django 5.0.6 on 2024-10-03 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipos', '0006_remove_equipofutbol_jugadores_historicos_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jugador',
            options={'verbose_name': 'Jugador', 'verbose_name_plural': 'Jugadores'},
        ),
    ]
