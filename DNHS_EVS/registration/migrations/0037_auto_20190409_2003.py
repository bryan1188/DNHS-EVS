# Generated by Django 2.1.5 on 2019-04-09 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0036_auto_20190409_1749'),
    ]

    operations = [
        migrations.RenameField(
            model_name='voter',
            old_name='is_voted_cased',
            new_name='is_vote_casted',
        ),
        migrations.AlterField(
            model_name='vote',
            name='hashed_id',
            field=models.CharField(default='ee3c59b2457e4646a64b66d4f894998d', max_length=255),
        ),
    ]
