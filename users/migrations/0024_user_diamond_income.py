# Generated by Django 2.2.4 on 2023-10-12 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_auto_20230926_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='diamond_income',
            field=models.FloatField(default=0),
        ),
    ]
