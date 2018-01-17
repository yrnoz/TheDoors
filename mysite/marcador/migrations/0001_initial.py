# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.CharField(max_length=9, serialize=False, verbose_name=b'user id', primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'user name')),
                ('access_permission', models.IntegerField(verbose_name=b'access_permission')),
                ('role', models.CharField(default=True, max_length=255, verbose_name=b'role')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'employee',
                'verbose_name_plural': 'employees',
            },
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.CharField(max_length=9, unique=True, serialize=False, primary_key=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'friend',
                'verbose_name_plural': 'friends',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('room_id', models.CharField(max_length=50)),
                ('num_employee', models.IntegerField()),
                ('date_time', models.DateField()),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'friend',
                'verbose_name_plural': 'friends',
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='friends',
            field=models.ManyToManyField(to='marcador.Friend', blank=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='schedule',
            field=models.ManyToManyField(to='marcador.Schedule', blank=True),
        ),
    ]
