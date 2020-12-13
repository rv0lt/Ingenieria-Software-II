# Generated by Django 3.1.2 on 2020-12-13 14:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0010_auto_20201213_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coche',
            name='calendario',
            field=models.JSONField(default="{datetime.date(2020, 12, 13), 'D'}"),
        ),
        migrations.AlterField(
            model_name='factura',
            name='fecha',
            field=models.DateTimeField(default=datetime.date.today, editable=False),
        ),
    ]
