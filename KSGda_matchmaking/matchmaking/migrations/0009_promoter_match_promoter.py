# Generated by Django 4.1.2 on 2022-10-13 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matchmaking', '0008_remove_match_players_match_players'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promoter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='promoter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='matchmaking.promoter'),
        ),
    ]