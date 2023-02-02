# Generated by Django 4.1.2 on 2023-01-04 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchmaking', '0041_alter_comments_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='red_cards',
            field=models.IntegerField(default=0, null=True, verbose_name='Czerwone kartki'),
        ),
        migrations.AddField(
            model_name='player',
            name='yellow_cards',
            field=models.IntegerField(default=0, null=True, verbose_name='Żółte kartki'),
        ),
    ]
