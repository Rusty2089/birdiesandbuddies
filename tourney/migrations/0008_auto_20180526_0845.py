# Generated by Django 2.0.2 on 2018-05-26 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourney', '0007_auto_20180526_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='isgolfing',
            field=models.NullBooleanField(default=True),
        ),
    ]
