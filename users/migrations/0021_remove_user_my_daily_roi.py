# Generated by Django 2.2 on 2023-07-26 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_auto_20230724_1024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='my_daily_roi',
        ),
    ]
