# Generated by Django 2.1.5 on 2019-04-13 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0020_auto_20190413_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ballot',
            name='voter_id_h',
            field=models.CharField(default='30123466ecac4cfbb311c722e3ea100d', max_length=255, unique=True, verbose_name='Hashed Voter ID'),
        ),
    ]
