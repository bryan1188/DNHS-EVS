# Generated by Django 2.1.5 on 2019-04-13 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0005_auto_20190413_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='denomarmalizedvotes',
            name='voter_id_h',
            field=models.CharField(default='97e4925961324b5e8ff29c5cce252575', max_length=255, unique=True, verbose_name='Hashed Voter ID'),
        ),
    ]
