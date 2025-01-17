# Generated by Django 3.1.2 on 2020-11-08 17:20

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0002_cliente_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coche',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(choices=[('A', 'Alta'), ('M', 'Media'), ('B', 'Baja')], max_length=1)),
                ('puertas', models.IntegerField(choices=[(3, 3), (5, 5)])),
                ('techo', models.CharField(choices=[('N', 'Normal'), ('C', 'Cabrio-Descapotable'), ('S', 'Solar-Panoramico')], max_length=1)),
                ('transmision', models.CharField(choices=[('M', 'Manual'), ('A', 'Automatico')], max_length=1)),
                ('estado', models.CharField(choices=[('D', 'Disponible'), ('M', 'Revision: Mantenimiento'), ('G', 'Revision: Golpe'), ('B', 'Baja'), ('R', 'Reservado')], default='D', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='cliente',
            name='edad',
            field=models.PositiveIntegerField(default=18),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='tipo',
            field=models.TextField(choices=[('P', 'Particular'), ('E', 'Empresa')], default='P', max_length=1),
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('fecha_reserva', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('fecha_objetivo', models.DateField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Backend.cliente')),
                ('coche', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Backend.coche')),
            ],
        ),
        migrations.CreateModel(
            name='Modelo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo', models.CharField(max_length=100, unique=True)),
                ('marca_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Backend.marca')),
            ],
        ),
        migrations.AddField(
            model_name='coche',
            name='modelo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Backend.modelo'),
        ),
    ]
