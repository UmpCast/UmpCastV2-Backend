# Generated by Django 3.0.7 on 2020-08-19 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0008_league_cancellation_period'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='league',
            name='opponent_library',
        ),
        migrations.RemoveField(
            model_name='league',
            name='ts_id',
        ),
    ]
