# Generated by Django 2.1.5 on 2019-04-13 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0041_auto_20190413_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='hashed_id',
            field=models.CharField(default='a48c659510a94d608c8133af937caece', max_length=255, unique=True),
        ),
    ]
