# Generated by Django 5.0.6 on 2024-06-23 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noticias', '0002_alter_noticias_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticias',
            name='imagen',
            field=models.ImageField(default=-3, upload_to='noticias/'),
            preserve_default=False,
        ),
    ]