# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-01 18:08
from __future__ import unicode_literals

import ckeditor_uploader.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_date_add', models.DateTimeField(auto_created=True, verbose_name='Дата создания')),
                ('article_title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('article_text', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Текст')),
                ('article_date_update', models.DateTimeField(default=datetime.datetime(2016, 4, 1, 21, 8, 34, 364994), verbose_name='Дата изминения')),
                ('article_likes', models.IntegerField(default=0, verbose_name='Понравилось')),
                ('article_dislikes', models.IntegerField(default=0, verbose_name='Не понравилось')),
                ('article_image', models.ImageField(blank=True, null=True, upload_to='image/', verbose_name='Картинка')),
                ('article_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name_plural': 'Статьи',
                'verbose_name': 'Статья',
                'ordering': ['-id'],
            },
        ),
    ]