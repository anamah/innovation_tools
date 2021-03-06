# Generated by Django 2.2.10 on 2020-04-19 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ocean',
            fields=[
                ('name', models.CharField(max_length=250, primary_key=True, serialize=False, verbose_name='name')),
                ('area', models.BigIntegerField(verbose_name='area')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('description', models.TextField(verbose_name='description')),
                ('map_url', models.URLField(verbose_name='map url')),
            ],
            options={
                'verbose_name': 'ocean',
                'verbose_name_plural': 'oceans',
                'ordering': ['name'],
            },
        ),
    ]
