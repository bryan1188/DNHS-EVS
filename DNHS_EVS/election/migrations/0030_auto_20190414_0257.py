# Generated by Django 2.1.5 on 2019-04-13 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0029_auto_20190414_0157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ballot',
            name='voter_id_h',
            field=models.CharField(default='52fb9454c75440f3b0ae428bc0ba74a6', max_length=255, unique=True, verbose_name='Hashed Voter ID'),
        ),
    ]
