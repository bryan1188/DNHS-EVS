# Generated by Django 2.1.5 on 2019-04-13 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0008_auto_20190413_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='denomarmalizedvotes',
            name='voter_id_h',
            field=models.CharField(default='0a46a061c2a0491da0f8bf66022b5906', max_length=255, unique=True, verbose_name='Hashed Voter ID'),
        ),
    ]
