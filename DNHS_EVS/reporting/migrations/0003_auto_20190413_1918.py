# Generated by Django 2.1.5 on 2019-04-13 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0002_auto_20190413_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='denomarmalizedvotes',
            name='voter_id_h',
            field=models.CharField(default='0b91eeed80e44e858eb858d6bd973195', max_length=255, unique=True, verbose_name='Hashed Voter ID'),
        ),
    ]
