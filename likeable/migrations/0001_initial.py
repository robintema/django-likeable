# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(help_text='The date/time when this user liked this object.', auto_now_add=True)),
                ('object_id', models.PositiveIntegerField(help_text='The primary key of the liked object.')),
                ('content_type', models.ForeignKey(help_text='The content type of the liked object.', to='contenttypes.ContentType')),
                ('user', models.ForeignKey(related_name='likes', to=settings.AUTH_USER_MODEL, help_text='The user who liked the particular object.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together=set([('user', 'content_type', 'object_id')]),
        ),
    ]
