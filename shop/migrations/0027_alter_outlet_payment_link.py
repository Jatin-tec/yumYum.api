# Generated by Django 4.2.4 on 2024-10-22 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0026_outlet_lite_outlet_payment_link_outletdocument'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outlet',
            name='payment_link',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]