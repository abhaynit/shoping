# Generated by Django 3.2.4 on 2021-09-11 10:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0015_auto_20210910_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mov_ticket',
            name='utm',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 11, 15, 45, 4, 925192)),
        ),
        migrations.CreateModel(
            name='select_halls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat', models.PositiveIntegerField()),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.cinema_hall')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.mov_ticket')),
            ],
        ),
    ]
