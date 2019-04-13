# Generated by Django 2.1.5 on 2019-04-13 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='denomarmalizedvotes',
            name='election_id',
            field=models.PositiveIntegerField(db_index=True, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='denomarmalizedvotes',
            name='voter_id_h',
            field=models.CharField(default='2405da0f597049babce5a331fa850632', max_length=255, unique=True, verbose_name='Hashed Voter ID'),
        ),
    ]
