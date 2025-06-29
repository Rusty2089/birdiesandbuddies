# Generated by Django 2.2.3 on 2020-05-30 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourney', '0034_auto_20200529_2323'),
    ]

    operations = [
        migrations.CreateModel(
            name='Extra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leader', models.CharField(max_length=30, null=True)),
                ('type', models.CharField(choices=[('Closest to the Pin', 'Closest to the Pin'), ('Long Drive', 'Long Drive')], max_length=30)),
                ('hole', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18)], default=0)),
            ],
        ),
    ]
