# Generated by Django 2.2.4 on 2023-07-08 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_user_total_income'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='my_achievement',
            field=models.CharField(default='NA', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='my_package',
            field=models.CharField(default='Inactive', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='my_rank',
            field=models.CharField(default='Inactive', max_length=100),
        ),
    ]