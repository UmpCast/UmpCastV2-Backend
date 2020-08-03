# Generated by Django 3.0.7 on 2020-07-31 07:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leagues', '0007_auto_20200731_0702'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('date_time', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('location', models.CharField(max_length=32)),
                ('description', models.TextField(blank=True, max_length=1028, null=True)),
                ('ts_id', models.IntegerField(default=0)),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leagues.Division')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True, max_length=1028, null=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.Game')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leagues.Role')),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('comments', models.TextField(blank=True, max_length=1028, null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
        ),
    ]