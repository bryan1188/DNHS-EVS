# Generated by Django 2.1.5 on 2019-04-17 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0022_auto_20190416_1835'),
    ]

    operations = [
        migrations.CreateModel(
            name='WinnerCandidateDenormalized',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('candidate_name', models.CharField(db_index=True, max_length=255, null=True, verbose_name='Candidate Name')),
                ('candidate_sex', models.CharField(db_index=True, max_length=1, verbose_name='Sex')),
                ('candidate_age', models.PositiveSmallIntegerField(blank=True, db_index=True, null=True, verbose_name='Age')),
                ('candidate_mother_tongue', models.CharField(db_index=True, max_length=50, verbose_name='Mother Tongue')),
                ('candidate_ethnic_group', models.CharField(db_index=True, max_length=50, verbose_name='Ethnic Group')),
                ('candidate_religion', models.CharField(db_index=True, max_length=100, verbose_name='Religion')),
                ('candidate_address_barangay', models.CharField(db_index=True, max_length=50, verbose_name='Address Barangay')),
                ('candidate_address_municipality', models.CharField(db_index=True, max_length=100, verbose_name='Address Municipality')),
                ('candidate_address_province', models.CharField(db_index=True, max_length=100, verbose_name='Address Province')),
                ('candidate_class_grade_level', models.CharField(db_index=True, max_length=20, null=True, verbose_name='Grade Level')),
                ('candidate_class_section', models.CharField(db_index=True, max_length=20, null=True, verbose_name='Section')),
                ('candidate_party', models.CharField(db_index=True, max_length=255, verbose_name='Pary Name')),
                ('candidate_position', models.CharField(db_index=True, max_length=100, verbose_name='Title')),
                ('candidate_position_number_of_slots', models.PositiveSmallIntegerField(verbose_name='Number of Slot')),
                ('candidate_position_priority', models.PositiveSmallIntegerField(db_index=True, default=0, verbose_name='Priority')),
                ('number_of_votes', models.PositiveIntegerField(default=0)),
                ('election_id', models.PositiveIntegerField(db_index=True)),
                ('election_name', models.CharField(db_index=True, max_length=255)),
                ('election_school_year', models.CharField(db_index=True, max_length=20, verbose_name='School Year')),
                ('election_day_from', models.DateField(db_index=True, verbose_name='Election Start Date')),
                ('election_day_to', models.DateField(db_index=True, verbose_name='Election End Date')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='denormalizedvotes',
            name='voter_id_h',
            field=models.CharField(default='7b5e289573e14a0287f4de74d4d32314', max_length=255, verbose_name='Hashed Voter ID'),
        ),
    ]