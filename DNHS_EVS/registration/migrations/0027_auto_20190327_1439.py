# Generated by Django 2.1.5 on 2019-03-27 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0026_auto_20190327_1438'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='candidate',
            unique_together={('student', 'election')},
        ),
    ]
