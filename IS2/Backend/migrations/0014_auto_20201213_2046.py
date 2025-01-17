# Generated by Django 3.1.2 on 2020-12-13 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0013_auto_20201213_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coche',
            name='calendario',
            field=models.JSONField(default="{'D', datetime.date(2020, 12, 13)}"),
        ),
        migrations.AlterField(
            model_name='factura',
            name='id_reserva',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Backend.reserva', unique=True),
        ),
    ]
