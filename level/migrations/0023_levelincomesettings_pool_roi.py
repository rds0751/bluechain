# Generated by Django 2.2 on 2023-07-26 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('level', '0022_auto_20230716_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='levelincomesettings',
            name='pool_roi',
            field=models.FloatField(default=0),
        ),
    ]
