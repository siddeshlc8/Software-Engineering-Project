# Generated by Django 2.0.3 on 2018-03-12 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0028_auto_20180312_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='toss_winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='toss_winner', to='tournament.Team'),
        ),
    ]