# Generated by Django 2.0.2 on 2018-03-04 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0006_auto_20180304_1650'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('innings', models.CharField(choices=[('First', 'First'), ('Second', 'Second')], default=None, max_length=11)),
                ('ball_number', models.IntegerField()),
                ('over_number', models.IntegerField()),
                ('run', models.IntegerField()),
                ('extra_type', models.CharField(choices=[('Wide', 'Wide'), ('NoBall', 'NoBall'), ('DeadBall', 'DeadBall')], default=None, max_length=11)),
                ('extra_run', models.IntegerField()),
                ('is_wicket', models.BooleanField(default=False)),
                ('wicket_type', models.CharField(choices=[('RunOut', 'RunOut'), ('Catch', 'Catch'), ('Bowled', 'Bowled'), ('Lbw', 'Lbw'), ('Stumps', 'Stumps'), ('HitWicket', 'HitWicket')], default=None, max_length=11)),
                ('batting_team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='batting_team', to='tournament.Team')),
                ('bowling_team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='bowling_team', to='tournament.Team')),
            ],
        ),
        migrations.AlterField(
            model_name='match',
            name='team_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='team_1', to='tournament.Team'),
        ),
        migrations.AddField(
            model_name='score',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.Match'),
        ),
    ]
