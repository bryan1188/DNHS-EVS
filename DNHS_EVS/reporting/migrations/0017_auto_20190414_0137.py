# Generated by Django 2.1.5 on 2019-04-13 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0016_auto_20190414_0137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='denomarmalizedvotes',
            name='voter_id_h',
            field=models.CharField(default='251d9a98e68c4199a5d14381b566c857', max_length=255, verbose_name='Hashed Voter ID'),
        ),
    ]
