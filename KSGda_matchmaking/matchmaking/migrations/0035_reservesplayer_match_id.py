# Generated by Django 4.1.2 on 2022-11-11 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matchmaking', '0034_playerrating_match_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservesplayer',
            name='match_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='matchmaking.match'),
        ),
    ]