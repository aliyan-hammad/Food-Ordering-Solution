# Generated by Django 5.1.1 on 2025-02-06 09:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_products_restaurant'),
        ('restaurant', '0015_alter_branch_address_delete_addresses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='restaurant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='restaurant.restaurant'),
        ),
    ]
