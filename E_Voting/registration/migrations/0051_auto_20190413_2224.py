# Generated by Django 2.1.5 on 2019-04-13 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0050_auto_20190413_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='hashed_id',
            field=models.CharField(default='f5182e6a5e73457a8b0d112283f4f3ce', max_length=255, unique=True),
        ),
    ]