# Generated by Django 5.2.2 on 2025-06-13 19:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_alter_bookissue_return_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookissue',
            name='return_date',
            field=models.DateField(default=datetime.datetime(2025, 6, 27, 19, 26, 34, 486213, tzinfo=datetime.timezone.utc)),
        ),
    ]
