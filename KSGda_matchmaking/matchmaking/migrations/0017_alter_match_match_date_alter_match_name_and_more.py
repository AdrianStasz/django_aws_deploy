# Generated by Django 4.1.2 on 2022-10-26 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchmaking', '0016_alter_match_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='match_date',
            field=models.DateTimeField(null=True, verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='match',
            name='name',
            field=models.CharField(max_length=200, null=True, verbose_name='Nazwa spotania'),
        ),
        migrations.AlterField(
            model_name='match',
            name='slots',
            field=models.IntegerField(null=True, verbose_name='Ilośc miejsc'),
        ),
    ]
