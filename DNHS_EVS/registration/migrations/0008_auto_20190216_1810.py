# Generated by Django 2.1.5 on 2019-02-16 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0007_auto_20190216_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='address_barangay',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.AddressBarangay', verbose_name='Address Barangay'),
        ),
        migrations.AddField(
            model_name='student',
            name='address_municipality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.AddressMunicipality', verbose_name='Address Municipality'),
        ),
        migrations.AddField(
            model_name='student',
            name='address_province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.AddressProvince', verbose_name='Address Province'),
        ),
        migrations.AddField(
            model_name='student',
            name='father_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name="Father's Name"),
        ),
        migrations.AddField(
            model_name='student',
            name='guardian_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name="Guardian's Name"),
        ),
        migrations.AddField(
            model_name='student',
            name='guardian_relationship',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Guardian Relationship'),
        ),
        migrations.AddField(
            model_name='student',
            name='mother_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name="Mother's Name"),
        ),
        migrations.AddField(
            model_name='student',
            name='parent_guardian_contact_no',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Parent Guardian Contact Number'),
        ),
        migrations.AddField(
            model_name='student',
            name='remarks',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Remarks'),
        ),
        migrations.AlterField(
            model_name='class',
            name='registered_female_bosy',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Registered Female BoSY'),
        ),
        migrations.AlterField(
            model_name='class',
            name='registered_female_eosy',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Registered Female EoSY'),
        ),
        migrations.AlterField(
            model_name='class',
            name='registered_male_bosy',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Registered Male BoSY'),
        ),
        migrations.AlterField(
            model_name='class',
            name='registered_male_eosy',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Registered Male EoSY'),
        ),
        migrations.AlterField(
            model_name='class',
            name='registered_total_bosy',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Registered Total EoSY'),
        ),
        migrations.AlterField(
            model_name='student',
            name='address_house_no',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Address House Number'),
        ),
        migrations.AlterField(
            model_name='student',
            name='middle_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Middle Name'),
        ),
    ]
