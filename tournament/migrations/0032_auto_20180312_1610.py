# Generated by Django 2.0.3 on 2018-03-12 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0031_auto_20180312_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='toss_winner_choice',
            field=models.CharField(default='Select', max_length=10),
        ),
    ]