# Generated by Django 3.1.5 on 2021-02-21 15:13

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('verifycertify', '0006_auto_20210213_1521'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewEventData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventName', models.CharField(max_length=20)),
                ('eventDescription', models.CharField(max_length=150)),
                ('date', models.DateField(default=datetime.date(2021, 2, 21))),
                ('proof1', models.FileField(upload_to='media/')),
                ('proof1AuthorisedBy', models.CharField(max_length=25)),
                ('proof2', models.FileField(upload_to='media/')),
                ('proof2AuthorisedBy', models.CharField(max_length=25)),
                ('proof3', models.FileField(upload_to='media/')),
                ('proof3AuthorisedBy', models.CharField(max_length=25)),
                ('proof4', models.FileField(upload_to='media/')),
                ('proof4AuthorisedBy', models.CharField(max_length=25)),
                ('proof5', models.FileField(upload_to='media/')),
                ('proof5AuthorisedBy', models.CharField(max_length=25)),
                ('totalParticipants', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
