# Generated by Django 2.1.5 on 2019-04-09 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0006_auto_20190409_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ballot',
            name='voter_id_h',
            field=models.CharField(default='b7d110f362344fc4a30c942480666e73', max_length=255, unique=True, verbose_name='Hashed Voter ID'),
        ),
    ]
