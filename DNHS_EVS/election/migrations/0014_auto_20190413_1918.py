# Generated by Django 2.1.5 on 2019-04-13 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0013_auto_20190413_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ballot',
            name='voter_id_h',
            field=models.CharField(default='de24d8588ce548c49457ca202a6689c5', max_length=255, unique=True, verbose_name='Hashed Voter ID'),
        ),
    ]