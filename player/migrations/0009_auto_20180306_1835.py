# Generated by Django 2.0.2 on 2018-03-06 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0008_player_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]