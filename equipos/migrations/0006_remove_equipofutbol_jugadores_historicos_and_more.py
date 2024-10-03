# Generated by Django 5.0.6 on 2024-10-03 16:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipos', '0005_jugador_remove_equipofutbol_jugadores_historicos_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipofutbol',
            name='jugadores_historicos',
        ),
        migrations.RemoveField(
            model_name='jugador',
            name='fecha_nacimiento',
        ),
        migrations.AddField(
            model_name='jugador',
            name='equipo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='jugadores', to='equipos.equipofutbol'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jugador',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='jugador',
            name='posicion',
            field=models.CharField(max_length=50),
        ),
    ]