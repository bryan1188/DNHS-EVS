# Generated by Django 2.1.5 on 2019-03-09 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_auto_20190308_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electionofficer',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_query_name='student', to='registration.Student', verbose_name='Student'),
        ),
    ]