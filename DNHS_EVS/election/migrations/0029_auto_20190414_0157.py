# Generated by Django 2.1.5 on 2019-04-13 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0028_auto_20190414_0137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ballot',
            name='voter_id_h',
            field=models.CharField(default='9090987d5ef24a9abd205f057dc41894', max_length=255, unique=True, verbose_name='Hashed Voter ID'),
        ),
    ]
