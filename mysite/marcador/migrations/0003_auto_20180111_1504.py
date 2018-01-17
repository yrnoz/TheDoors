# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marcador', '0002_employee_password'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schedule',
            options={'ordering': ['room_id'], 'verbose_name': 'schedule', 'verbose_name_plural': 'schedules'},
        ),
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.CharField(max_length=255, verbose_name=b'role'),
        ),
    ]
