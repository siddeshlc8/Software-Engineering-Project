# Generated by Django 2.0.1 on 2018-03-15 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0031_battinginnings_bowlinginnings_performancematch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bowlinginnings',
            name='status',
        ),
        migrations.AddField(
            model_name='performancematch',
            name='status',
            field=models.CharField(default=False, max_length=20),
            preserve_default=False,
        ),
    ]
