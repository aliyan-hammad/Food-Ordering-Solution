# Generated by Django 5.1.1 on 2025-01-07 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_rename_cost_products_price_products_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
