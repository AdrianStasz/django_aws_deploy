# Generated by Django 4.1.2 on 2022-10-11 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchmaking', '0005_alter_player_favorite_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='players',
            field=models.ManyToManyField(to='matchmaking.player'),
        ),
    ]
