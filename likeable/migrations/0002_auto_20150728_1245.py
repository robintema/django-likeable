# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('likeable', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='object_id',
            field=models.CharField(help_text='The primary key of the liked object.', max_length=250),
            preserve_default=True,
        ),
    ]
