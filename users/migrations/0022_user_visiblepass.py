# Generated by Django 2.2 on 2023-08-02 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_remove_user_my_daily_roi'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='visiblepass',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]