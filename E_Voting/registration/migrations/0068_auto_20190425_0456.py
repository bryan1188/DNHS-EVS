# Generated by Django 2.1.5 on 2019-04-24 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0067_auto_20190419_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='grade_level_integer',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='general_plan_of_actions',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='General Plan of Actions'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='hashed_id',
            field=models.CharField(default='64aaa532a00f47c19f6dc7bcc286a280', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='votearchived',
            name='hashed_id',
            field=models.CharField(default='0898dc624edd490198a95d0da8d337a4', max_length=255, unique=True),
        ),
    ]