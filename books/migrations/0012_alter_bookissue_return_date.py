# Generated by Django 5.2.2 on 2025-06-15 17:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0011_alter_bookissue_return_date_fine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookissue',
            name='return_date',
            field=models.DateField(default=datetime.datetime(2025, 6, 29, 17, 26, 10, 819513, tzinfo=datetime.timezone.utc)),
        ),
    ]
