# Generated by Django 2.0.1 on 2018-03-14 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0022_performancematchwise_bowling_balls'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performancematchwise',
            name='bowling_balls',
        ),
    ]