# Generated by Django 2.1.5 on 2019-04-13 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0014_auto_20190413_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='denomarmalizedvotes',
            name='voter_id_h',
            field=models.CharField(default='c67cb1e87dcf428a8014c588143c00c9', max_length=255, verbose_name='Hashed Voter ID'),
        ),
    ]
