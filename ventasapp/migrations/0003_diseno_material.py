# Generated by Django 4.1.7 on 2023-06-26 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventasapp', '0002_alter_ventanorealizada_bodega_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diseno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=30)),
                ('descripcion', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=30)),
                ('descripcion', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
    ]
