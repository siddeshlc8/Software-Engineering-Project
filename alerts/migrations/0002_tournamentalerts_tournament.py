# Generated by Django 2.0.1 on 2018-03-24 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tournament', '0001_initial'),
        ('alerts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournamentalerts',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.Tournament'),
        ),
    ]
