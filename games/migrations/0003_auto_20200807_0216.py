# Generated by Django 3.0.7 on 2020-08-07 02:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20200802_0440'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ['-date_time']},
        ),
    ]
