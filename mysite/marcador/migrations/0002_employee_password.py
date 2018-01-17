# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marcador', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='password',
            field=models.CharField(default=123, max_length=255, verbose_name=b'password'),
            preserve_default=False,
        ),
    ]
