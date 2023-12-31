# Generated by Django 2.2.4 on 2023-07-08 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_user_c'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='autopool_income',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='lifetime_royalty',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='my_daily_roi',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='my_directs',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='my_team',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='pool_wallet',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='rewards',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='sponsor_income',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='team_club_income',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='today_income',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='total_business',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='wallet',
            field=models.FloatField(default=0),
        ),
    ]
