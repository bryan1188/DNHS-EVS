# Generated by Django 2.1.5 on 2019-04-13 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0042_auto_20190413_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='hashed_id',
            field=models.CharField(default='d92aa43fad8e401bb2197f580807f684', max_length=255, unique=True),
        ),
    ]
