# Generated by Django 2.1.5 on 2019-03-13 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0012_auto_20190313_1323'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('number_of_slots', models.PositiveSmallIntegerField(verbose_name='Number of Slot')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active?')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
