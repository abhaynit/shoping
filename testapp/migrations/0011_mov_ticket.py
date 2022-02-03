# Generated by Django 3.2.4 on 2021-09-04 12:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0010_auto_20210904_1728'),
    ]

    operations = [
        migrations.CreateModel(
            name='mov_ticket',
            fields=[
                ('mname', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='media')),
                ('orig', models.DecimalField(decimal_places=2, max_digits=10)),
                ('disp', models.DecimalField(decimal_places=2, max_digits=10)),
                ('utm', models.DateTimeField(default=datetime.datetime(2021, 9, 4, 17, 39, 32, 983951))),
            ],
        ),
    ]
