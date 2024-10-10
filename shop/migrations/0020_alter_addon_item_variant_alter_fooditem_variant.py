# Generated by Django 4.2.4 on 2024-10-10 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_alter_discountcoupon_valid_from_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addon',
            name='item_variant',
            field=models.ManyToManyField(related_name='addons', to='shop.itemvariant'),
        ),
        migrations.AlterField(
            model_name='fooditem',
            name='variant',
            field=models.ManyToManyField(related_name='food_items', to='shop.variantcategory'),
        ),
    ]
