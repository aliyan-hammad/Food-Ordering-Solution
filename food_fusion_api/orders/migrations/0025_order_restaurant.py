# Generated by Django 5.1.1 on 2025-02-12 20:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0024_rename_products_cartitem_product_and_more'),
        ('restaurant', '0016_restaurant_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.branch'),
        ),
    ]
