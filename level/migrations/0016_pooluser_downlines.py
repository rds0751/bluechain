# Generated by Django 2.2.4 on 2023-07-07 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('level', '0015_pooluser_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='pooluser',
            name='downlines',
            field=models.IntegerField(default=0),
        ),
    ]
