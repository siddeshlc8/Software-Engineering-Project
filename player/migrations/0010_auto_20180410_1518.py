# Generated by Django 2.0.1 on 2018-04-10 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0009_auto_20180327_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='image',
            field=models.ImageField(default='players/no.png', upload_to='players'),
        ),
    ]
