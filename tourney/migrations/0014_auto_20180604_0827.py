# Generated by Django 2.0.2 on 2018-06-04 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourney', '0013_auto_20180527_1840'),
    ]

    operations = [
        migrations.CreateModel(
            name='Daily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=15, unique=True)),
                ('grouping', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0)),
                ('quota', models.PositiveSmallIntegerField(default=0)),
                ('h1_pts', models.PositiveSmallIntegerField(choices=[('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)])),
                ('h2_pts', models.PositiveSmallIntegerField(choices=[('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)])),
                ('h3_pts', models.PositiveSmallIntegerField(choices=[('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)])),
                ('h4_pts', models.PositiveSmallIntegerField(choices=[('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)])),
                ('h5_pts', models.PositiveSmallIntegerField(choices=[('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)])),
                ('h6_pts', models.PositiveSmallIntegerField(choices=[('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)])),
                ('h7_pts', models.PositiveSmallIntegerField(choices=[('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)])),
                ('h8_pts', models.PositiveSmallIntegerField(choices=[('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)])),
                ('h9_pts', models.PositiveSmallIntegerField(choices=[('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)])),
                ('h10_pts', models.PositiveSmallIntegerField(choices=[('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)])),
                ('h11_pts', models.PositiveSmallIntegerField(choices=[('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)])),
                ('h12_pts', models.PositiveSmallIntegerField(choices=[('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)])),
                ('h13_pts', models.PositiveSmallIntegerField(choices=[('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)])),
                ('h14_pts', models.PositiveSmallIntegerField(choices=[('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)])),
                ('h15_pts', models.PositiveSmallIntegerField(choices=[('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)])),
                ('h16_pts', models.PositiveSmallIntegerField(choices=[('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)])),
                ('h17_pts', models.PositiveSmallIntegerField(choices=[('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)])),
                ('h18_pts', models.PositiveSmallIntegerField(choices=[('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)])),
                ('raw_day_points', models.PositiveSmallIntegerField()),
                ('net_day_points', models.SmallIntegerField()),
                ('net_tourney_score', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RoundData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_round', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3)])),
                ('group1_ttime', models.TimeField()),
                ('group2_ttime', models.TimeField()),
                ('group3_ttime', models.TimeField()),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='r1_group',
            field=models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='r2_group',
            field=models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='r3_group',
            field=models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0),
        ),
    ]
