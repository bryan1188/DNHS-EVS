# Generated by Django 2.1.5 on 2019-04-09 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0006_auto_20190409_1749'),
        ('registration', '0035_auto_20190409_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='hashed_id',
            field=models.CharField(default='f9f3e523feda4638b04f61222b332608', max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('ballot', 'candidate')},
        ),
    ]