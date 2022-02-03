# Generated by Django 3.2.4 on 2021-09-19 13:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0016_auto_20210911_1545'),
    ]

    operations = [
        migrations.DeleteModel(
            name='bas',
        ),
        migrations.DeleteModel(
            name='calle',
        ),
        migrations.RemoveField(
            model_name='select_hall',
            name='hall',
        ),
        migrations.RemoveField(
            model_name='select_hall',
            name='movie',
        ),
        migrations.AlterField(
            model_name='mov_ticket',
            name='utm',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 19, 18, 50, 8, 663190)),
        ),
        migrations.DeleteModel(
            name='hal_nam',
        ),
        migrations.DeleteModel(
            name='select_hall',
        ),
    ]
