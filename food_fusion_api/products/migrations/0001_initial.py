# Generated by Django 5.1.1 on 2024-12-26 02:17

import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('restaurant', '0004_alter_address_restaurant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('catagory', models.CharField(choices=[('barBQ', 'Barbq'), ('fastfood', 'Fastfood'), ('chiniesfood', 'Chiniesfood'), ('pakistanifood', 'Pakistanifood')], default='None', max_length=50)),
                ('cost', models.DecimalField(decimal_places=2, default=Decimal('99.99'), max_digits=10)),
                ('content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('restaurant', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='restaurant.restaurant')),
            ],
        ),
    ]
