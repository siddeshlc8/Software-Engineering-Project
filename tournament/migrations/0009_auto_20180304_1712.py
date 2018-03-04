# Generated by Django 2.0.2 on 2018-03-04 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0008_auto_20180304_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='extra_type',
            field=models.CharField(choices=[('Wide', 'Wide'), ('NoBall', 'NoBall'), ('DeadBall', 'DeadBall')], default=None, max_length=11),
        ),
        migrations.AlterField(
            model_name='score',
            name='wicket_type',
            field=models.CharField(choices=[('RunOut', 'RunOut'), ('Catch', 'Catch'), ('Bowled', 'Bowled'), ('Lbw', 'Lbw'), ('Stumps', 'Stumps'), ('HitWicket', 'HitWicket')], default=None, max_length=11),
        ),
    ]
