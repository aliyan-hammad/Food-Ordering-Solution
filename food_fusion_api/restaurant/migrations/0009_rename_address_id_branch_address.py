# Generated by Django 5.1.1 on 2024-12-29 23:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0008_rename_closs_time_restaurant_close_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='branch',
            old_name='address_id',
            new_name='address',
        ),
    ]
