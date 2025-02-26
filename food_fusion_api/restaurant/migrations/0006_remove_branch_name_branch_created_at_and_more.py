# Generated by Django 5.1.1 on 2024-12-28 09:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0005_branch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branch',
            name='name',
        ),
        migrations.AddField(
            model_name='branch',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 28, 1, 36, 50, 382776)),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Karachi', 'Karachi'), ('Islamabad', 'Islamabad'), ('Rawalpindi', 'Rawalpindi'), ('Lahore', 'Lahore'), ('Hyderabad', 'Hyderabad'), ('Multan', 'Multan')], max_length=100),
        ),
    ]
