# Generated by Django 2.1.5 on 2019-04-09 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ballot',
            name='voter_id_h',
            field=models.CharField(default='Empty', max_length=255, verbose_name='Hashed Voter ID'),
        ),
    ]
