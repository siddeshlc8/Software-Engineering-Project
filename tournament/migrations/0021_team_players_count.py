# Generated by Django 2.0.3 on 2018-03-11 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0020_auto_20180311_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='players_count',
            field=models.IntegerField(default=0),
        ),
    ]
