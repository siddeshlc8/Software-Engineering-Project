# Generated by Django 2.0.3 on 2018-03-12 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0032_auto_20180312_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='toss_stored',
            field=models.BooleanField(default=False),
        ),
    ]