# Generated by Django 3.0.7 on 2020-08-19 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamsnap', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamsnapnote',
            name='note_type',
            field=models.CharField(choices=[('sync', 'sync'), ('build', 'build')], default='sync', max_length=5),
            preserve_default=False,
        ),
    ]
