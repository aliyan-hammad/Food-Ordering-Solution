# Generated by Django 5.1.1 on 2025-02-06 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_orderitems_user_alter_orderitems_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkout',
            name='user',
        ),
    ]
