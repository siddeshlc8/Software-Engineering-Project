# Generated by Django 2.0.3 on 2018-03-27 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0002_auto_20180324_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizer',
            name='image',
            field=models.ImageField(blank=True, upload_to='organizers'),
        ),
    ]
