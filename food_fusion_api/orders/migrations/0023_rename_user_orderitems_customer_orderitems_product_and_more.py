# Generated by Django 5.1.1 on 2025-02-12 19:41

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_rename_addresses_address'),
        ('orders', '0022_remove_checkout_cart_data_cart_ordered'),
        ('products', '0007_alter_products_restaurant'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitems',
            old_name='user',
            new_name='customer',
        ),
        migrations.AddField(
            model_name='orderitems',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='products.products'),
        ),
        migrations.AddField(
            model_name='orderitems',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False, unique=True)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_status', models.CharField(default='Pending', max_length=100)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('delevered_at', models.DateTimeField(blank=True, null=True)),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='address.address')),
            ],
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='orders.order'),
        ),
        migrations.DeleteModel(
            name='Checkout',
        ),
    ]
