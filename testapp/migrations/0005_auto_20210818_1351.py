# Generated by Django 3.2.4 on 2021-08-18 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0004_carted'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ab',
        ),
        migrations.DeleteModel(
            name='cart',
        ),
    ]
