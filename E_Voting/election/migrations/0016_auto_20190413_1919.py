# Generated by Django 2.1.5 on 2019-04-13 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0015_auto_20190413_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ballot',
            name='voter_id_h',
            field=models.CharField(default='3f82f22858994562b4163deb3f1b0ad6', max_length=255, unique=True, verbose_name='Hashed Voter ID'),
        ),
    ]
