# Generated by Django 3.2.4 on 2021-09-10 06:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0014_auto_20210909_1444'),
    ]

    operations = [
        migrations.CreateModel(
            name='bas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lef', models.PositiveIntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='mov_ticket',
            name='utm',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 10, 12, 27, 6, 862778)),
        ),
    ]
