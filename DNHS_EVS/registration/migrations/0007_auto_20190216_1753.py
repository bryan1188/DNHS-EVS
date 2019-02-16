# Generated by Django 2.1.5 on 2019-02-16 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='address_house_no',
            field=models.CharField(blank=True, max_length=50, verbose_name='Address House Number'),
        ),
        migrations.AddField(
            model_name='student',
            name='age',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Age'),
        ),
        migrations.AddField(
            model_name='student',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='Birth Date'),
        ),
        migrations.AddField(
            model_name='student',
            name='ethnic_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.EthnicGroup', verbose_name='Ethnic Group'),
        ),
        migrations.AddField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=50, null=True, verbose_name='First Name'),
        ),
        migrations.AddField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=50, null=True, verbose_name='Last Name'),
        ),
        migrations.AddField(
            model_name='student',
            name='middle_name',
            field=models.CharField(max_length=50, null=True, verbose_name='Middle Name'),
        ),
        migrations.AddField(
            model_name='student',
            name='mother_tounge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.MotherTounge', verbose_name='Mother Tounge'),
        ),
        migrations.AddField(
            model_name='student',
            name='religion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.Religion', verbose_name='Religion'),
        ),
        migrations.AddField(
            model_name='student',
            name='sex',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.Sex', verbose_name='Sex'),
        ),
        migrations.AlterField(
            model_name='class',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.School', verbose_name='School'),
        ),
        migrations.AlterField(
            model_name='school',
            name='principal_name',
            field=models.CharField(max_length=150, verbose_name='Principal Name'),
        ),
    ]
