# Generated by Django 2.1.5 on 2019-03-10 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_auto_20190309_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]