# Generated by Django 3.1.5 on 2021-02-13 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifycertify', '0004_auto_20210213_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extraprofiledata',
            name='approved',
            field=models.IntegerField(choices=[(0, 'pending'), (1, 'approved'), (2, 'rejected')], default=0, max_length=1),
        ),
    ]