# Generated by Django 4.1.2 on 2022-10-25 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchmaking', '0010_player_user_promoter_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='promoter',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
