# Generated by Django 4.1.2 on 2022-11-09 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchmaking', '0028_remove_player_date_to_sort_by_reservesplayer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserves',
            name='players',
            field=models.ManyToManyField(to='matchmaking.player'),
        ),
        migrations.DeleteModel(
            name='ReservesPlayer',
        ),
    ]