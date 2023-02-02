# Generated by Django 4.1.2 on 2022-10-26 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchmaking', '0017_alter_match_match_date_alter_match_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='status',
            field=models.CharField(choices=[('Nie wystartował', 'Nie wystartował'), ('W trakcie', 'W trakcie'), ('Zakończony', 'Zakończony')], max_length=200, null=True, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='player',
            name='email',
            field=models.CharField(max_length=200, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='player',
            name='favorite_position',
            field=models.CharField(choices=[('Bramkarz', 'Bramkarz'), ('Obrońca', 'Obrońca'), ('Pomocnik', 'Pomocnik'), ('Napastnik', 'Napastnik')], max_length=200, null=True, verbose_name='Ulubiona pozycja'),
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(max_length=200, null=True, verbose_name='Imię/nazwisko'),
        ),
        migrations.AlterField(
            model_name='player',
            name='nickname',
            field=models.CharField(max_length=200, null=True, verbose_name='Ksywka'),
        ),
        migrations.AlterField(
            model_name='player',
            name='phone',
            field=models.CharField(max_length=200, null=True, verbose_name='Nr telefonu'),
        ),
        migrations.AlterField(
            model_name='promoter',
            name='email',
            field=models.CharField(max_length=200, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='promoter',
            name='name',
            field=models.CharField(max_length=200, null=True, verbose_name='Imię/nazwisko'),
        ),
        migrations.AlterField(
            model_name='promoter',
            name='phone',
            field=models.CharField(max_length=200, null=True, verbose_name='Nr telefonu'),
        ),
    ]