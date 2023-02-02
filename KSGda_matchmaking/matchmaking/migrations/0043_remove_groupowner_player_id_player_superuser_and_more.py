# Generated by Django 4.1.2 on 2023-01-05 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchmaking', '0042_player_red_cards_player_yellow_cards'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupowner',
            name='player_id',
        ),
        migrations.AddField(
            model_name='player',
            name='superuser',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.DeleteModel(
            name='GroupOwner',
        ),
    ]
