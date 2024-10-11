# Generated by Django 4.2.4 on 2024-10-10 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_alter_addon_item_variant_alter_fooditem_variant'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderTimelineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.CharField(max_length=100)),
                ('done', models.BooleanField(default=False)),
                ('content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timeline', to='shop.order')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]