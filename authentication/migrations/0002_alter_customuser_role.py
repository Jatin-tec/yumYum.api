# Generated by Django 4.2.4 on 2024-08-30 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('customer', 'Customer'), ('owner', 'Owner'), ('admin', 'Admin'), ('outlet_manager', 'Outlet Manager')], max_length=20),
        ),
    ]