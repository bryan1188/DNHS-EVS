# Generated by Django 2.1.5 on 2019-04-13 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0030_auto_20190414_0257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ballot',
            name='voter_id_h',
            field=models.CharField(default='25d2b4e541b149469ecac871a2e080a6', max_length=255, unique=True, verbose_name='Hashed Voter ID'),
        ),
    ]
