# Generated by Django 3.0.7 on 2020-07-29 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='default_max_backup',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='league',
            name='default_max_cast',
            field=models.IntegerField(default=0),
        ),
    ]
