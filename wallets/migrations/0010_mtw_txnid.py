# Generated by Django 2.2.4 on 2023-07-18 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0009_auto_20230714_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='mtw',
            name='txnid',
            field=models.CharField(default='drftgvbh', max_length=125),
        ),
    ]
