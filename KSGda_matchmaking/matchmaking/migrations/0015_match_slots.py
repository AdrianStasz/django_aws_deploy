# Generated by Django 4.1.2 on 2022-10-26 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchmaking', '0014_promoter_player_alter_match_promoter_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='slots',
            field=models.IntegerField(null=True),
        ),
    ]
