# Generated by Django 5.1.1 on 2025-01-30 16:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
        ('orders', '0010_alter_orderitems_delievery_address'),
        ('restaurant', '0014_addresses_updated_at_alter_addresses_address_lane2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch', to='address.addresses'),
        ),
        migrations.DeleteModel(
            name='Addresses',
        ),
    ]
