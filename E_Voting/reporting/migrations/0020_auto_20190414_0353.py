# Generated by Django 2.1.5 on 2019-04-13 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0019_auto_20190414_0257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='denomarmalizedvotes',
            name='voter_id_h',
            field=models.CharField(default='c1dca18a18c14a59b65057356576594d', max_length=255, verbose_name='Hashed Voter ID'),
        ),
    ]