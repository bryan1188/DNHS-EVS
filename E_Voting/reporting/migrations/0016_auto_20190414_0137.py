# Generated by Django 2.1.5 on 2019-04-13 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0015_auto_20190414_0137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='denomarmalizedvotes',
            name='voter_id_h',
            field=models.CharField(default='2d1feb78a24740beb59ec55e4d53e482', max_length=255, verbose_name='Hashed Voter ID'),
        ),
    ]