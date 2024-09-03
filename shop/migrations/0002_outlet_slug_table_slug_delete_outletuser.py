# Generated by Django 4.2.4 on 2024-08-31 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='outlet',
            name='slug',
            field=models.SlugField(default='outlet', max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='table',
            name='slug',
            field=models.SlugField(default='table', max_length=100, unique=True),
        ),
        migrations.DeleteModel(
            name='OutletUser',
        ),
    ]