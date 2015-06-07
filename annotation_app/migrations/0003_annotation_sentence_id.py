# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotation_app', '0002_auto_20150606_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='sentence_id',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
