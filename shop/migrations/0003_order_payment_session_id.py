# Generated by Django 4.2.4 on 2024-09-17 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_order_options_order_payment_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_session_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
