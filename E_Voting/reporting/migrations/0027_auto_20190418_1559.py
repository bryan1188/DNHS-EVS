# Generated by Django 2.1.5 on 2019-04-18 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0026_auto_20190418_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='denormalizedvotes',
            name='voter_id_h',
            field=models.CharField(default='fa4262843b9e4b4b89d3c6ef97fd2c2e', max_length=255, verbose_name='Hashed Voter ID'),
        ),
    ]