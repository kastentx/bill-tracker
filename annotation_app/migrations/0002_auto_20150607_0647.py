# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotation_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Senator',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('committee', models.CharField(max_length=255)),
                ('is_chair', models.BooleanField()),
            ],
        ),
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
        migrations.AddField(
            model_name='annotation',
            name='sentence_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='bill',
            name='caption_text',
            field=models.TextField(default='null'),
        ),
        migrations.AddField(
            model_name='bill',
            name='caption_version',
            field=models.CharField(max_length=255, default='null'),
        ),
        migrations.AddField(
            model_name='bill',
            name='coauthor',
            field=models.CharField(max_length=255, default='null'),
        ),
        migrations.AddField(
            model_name='bill',
            name='cosponsor',
            field=models.CharField(max_length=255, default='null'),
        ),
        migrations.AddField(
            model_name='bill',
            name='last_action',
            field=models.CharField(max_length=255, default='null'),
        ),
        migrations.AddField(
            model_name='bill',
            name='number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bill',
            name='origin',
            field=models.CharField(max_length=255, default='null'),
        ),
        migrations.AddField(
            model_name='bill',
            name='sponsor',
            field=models.CharField(max_length=255, default='null'),
        ),
        migrations.AddField(
            model_name='bill',
            name='stage',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bill',
            name='subjects',
            field=models.TextField(default='null'),
        ),
        migrations.AddField(
            model_name='senator',
            name='bills',
            field=models.ManyToManyField(to='annotation_app.Bill'),
        ),
    ]
