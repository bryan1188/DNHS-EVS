# Generated by Django 2.1.5 on 2019-04-13 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0039_auto_20190413_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='hashed_id',
            field=models.CharField(default='959f1f7eb3c3465eae86f633f010d779', max_length=255, unique=True),
        ),
    ]
