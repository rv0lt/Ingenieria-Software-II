# Generated by Django 3.1.2 on 2020-12-13 14:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0009_auto_20201213_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='fecha',
            field=models.DateField(default=datetime.date(2020, 12, 13), editable=False),
        ),
    ]
