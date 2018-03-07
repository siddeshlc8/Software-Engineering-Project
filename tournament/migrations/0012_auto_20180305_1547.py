# Generated by Django 2.0.2 on 2018-03-05 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0011_match_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='extra_type',
            field=models.CharField(choices=[('Wide', 'Wide'), ('NoBall', 'NoBall'), ('DeadBall', 'DeadBall')], max_length=11),
        ),
    ]