# Generated by Django 5.1.1 on 2025-01-03 10:42

import datetime
import django.db.models.deletion
import django.utils.timezone
import food_fusion_api.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0012_remove_addresses_mainstreet_remove_addresses_plot_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='close_time',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='open_time',
        ),
        migrations.AddField(
            model_name='branch',
            name='close_time',
            field=models.TimeField(default=datetime.time(23, 59)),
        ),
        migrations.AddField(
            model_name='branch',
            name='contact',
            field=models.CharField(max_length=11, null=True, validators=[food_fusion_api.validators.validator_contact]),
        ),
        migrations.AddField(
            model_name='branch',
            name='open_time',
            field=models.TimeField(default=datetime.time(9, 0)),
        ),
        migrations.AddField(
            model_name='branch',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='addresses',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 3, 15, 40, 36, 884916)),
        ),
        migrations.AlterField(
            model_name='branch',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch', to='restaurant.addresses'),
        ),
    ]
