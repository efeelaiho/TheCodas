# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Albums',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('release_date', models.DateField()),
                ('genre', models.CharField(max_length=50)),
                ('spotify_href', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('origin', models.CharField(max_length=50)),
                ('popularity', models.IntegerField()),
                ('genre', models.CharField(max_length=50)),
                ('spotify_href', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='albums',
            name='artist',
            field=models.ForeignKey(to='volumemax.Artist'),
        ),
    ]
