# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marcador', '0003_auto_20180111_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='friends',
            field=models.ManyToManyField(related_name='friends', to='marcador.Friend', blank=True),
        ),
    ]
