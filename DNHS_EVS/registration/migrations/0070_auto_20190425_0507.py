# Generated by Django 2.1.5 on 2019-04-24 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0069_auto_20190425_0504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='hashed_id',
            field=models.CharField(default='fc9f3ae9a6b54656bbe184464872e2a1', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='votearchived',
            name='hashed_id',
            field=models.CharField(default='57313f8789274bc4b88e0c0b97888631', max_length=255, unique=True),
        ),
    ]