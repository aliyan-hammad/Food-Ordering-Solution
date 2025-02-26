# Generated by Django 5.1.1 on 2025-01-20 09:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_products_updated_at'),
        ('restaurant', '0014_addresses_updated_at_alter_addresses_address_lane2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='restaurant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='restaurant.restaurant'),
        ),
    ]
