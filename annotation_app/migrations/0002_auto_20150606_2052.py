# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotation_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='annotation',
            old_name='reporter',
            new_name='bill_id',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='reporter',
            new_name='annotation_id',
        ),
    ]
