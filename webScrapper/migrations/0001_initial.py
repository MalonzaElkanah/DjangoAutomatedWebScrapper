# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-09-13 07:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scrapper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_scrapped', models.CharField(max_length=1000, verbose_name='url')),
                ('select_tag', models.CharField(max_length=100, verbose_name='Select Tag')),
                ('data_type', models.CharField(default='TEXT', max_length=10, verbose_name='Data Type')),
            ],
        ),
        migrations.CreateModel(
            name='ScrapperRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_scrapped', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('data_scrapped', models.FileField(max_length=100000, upload_to='File/Data/ScrappedFiles', verbose_name='Data File')),
                ('status', models.CharField(max_length=10, verbose_name='Status')),
                ('category', models.CharField(default='not_view', max_length=20, verbose_name='Category')),
                ('scrapper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webScrapper.Scrapper')),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=50, verbose_name='Site')),
                ('logo', models.ImageField(default='dummy.png', upload_to='Image/Data/Logo', verbose_name='Logo')),
                ('ip_address', models.CharField(blank=True, max_length=20, null=True, verbose_name='IP ip_address')),
                ('category', models.CharField(max_length=100, verbose_name='Select Tag')),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='Description')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
            ],
        ),
        migrations.AddField(
            model_name='scrapper',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webScrapper.Site'),
        ),
    ]
