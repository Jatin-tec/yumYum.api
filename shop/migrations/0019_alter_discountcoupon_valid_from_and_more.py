# Generated by Django 4.2.4 on 2024-10-05 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_discountcoupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountcoupon',
            name='valid_from',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='discountcoupon',
            name='valid_to',
            field=models.DateField(),
        ),
    ]