# Generated by Django 2.1.5 on 2019-03-16 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0016_auto_20190315_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='positions',
            field=models.ManyToManyField(blank=True, related_name='elections', to='registration.Position', verbose_name='Positions'),
        ),
    ]
