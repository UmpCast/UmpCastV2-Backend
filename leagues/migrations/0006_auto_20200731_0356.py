# Generated by Django 3.0.7 on 2020-07-31 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0005_auto_20200730_2047'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='division',
            options={'ordering': ('order',)},
        ),
        migrations.AlterModelOptions(
            name='role',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='division',
            name='order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False, verbose_name='order'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='role',
            name='order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False, verbose_name='order'),
            preserve_default=False,
        ),
    ]
