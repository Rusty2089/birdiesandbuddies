# Generated by Django 2.0.2 on 2018-05-21 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourney', '0002_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='City',
            field=models.CharField(default='City', max_length=20),
        ),
        migrations.AddField(
            model_name='user',
            name='handicap',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.CharField(default='FL', max_length=2),
        ),
        migrations.AddField(
            model_name='user',
            name='user_id',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
