# Generated by Django 3.1.2 on 2020-11-09 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0005_auto_20201108_1951'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='contrasena',
            field=models.CharField(default='xXx_default_xXx', max_length=30),
            preserve_default=False,
        ),
    ]
