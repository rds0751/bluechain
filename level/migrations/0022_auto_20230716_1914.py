# Generated by Django 2.2.4 on 2023-07-16 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('level', '0021_levelincomesettings_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pooluser',
            name='user',
            field=models.CharField(blank=True, max_length=25, null=True, unique=True),
        ),
    ]