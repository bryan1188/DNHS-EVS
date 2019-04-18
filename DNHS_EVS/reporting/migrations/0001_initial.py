# Generated by Django 2.1.5 on 2019-04-13 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DenomarmalizedVotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('voter_id_h', models.CharField(default='eeb813c8784a42439c8cfdafbf9caea7', max_length=255, unique=True, verbose_name='Hashed Voter ID')),
                ('voter_sex', models.CharField(db_index=True, max_length=1, verbose_name='Sex')),
                ('voter_age', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Age')),
                ('voter_mother_tongue', models.CharField(db_index=True, max_length=50, verbose_name='Mother Tongue')),
                ('voter_ethnic_group', models.CharField(db_index=True, max_length=50, verbose_name='Ethnic Group')),
                ('voter_religion', models.CharField(db_index=True, max_length=100, verbose_name='Religion')),
                ('voter_address_barangay', models.CharField(db_index=True, max_length=50, verbose_name='Address Barangay')),
                ('voter_address_municipality', models.CharField(db_index=True, max_length=100, verbose_name='Address Municipality')),
                ('voter_address_province', models.CharField(db_index=True, max_length=100, verbose_name='Address Province')),
                ('candidate_sex', models.CharField(db_index=True, max_length=1, verbose_name='Sex')),
                ('candidate_age', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Age')),
                ('candidate_mother_tongue', models.CharField(db_index=True, max_length=50, verbose_name='Mother Tongue')),
                ('candidate_ethnic_group', models.CharField(db_index=True, max_length=50, verbose_name='Ethnic Group')),
                ('candidate_religion', models.CharField(db_index=True, max_length=100, verbose_name='Religion')),
                ('candidate_address_barangay', models.CharField(db_index=True, max_length=50, verbose_name='Address Barangay')),
                ('candidate_address_municipality', models.CharField(db_index=True, max_length=100, verbose_name='Address Municipality')),
                ('candidate_address_province', models.CharField(db_index=True, max_length=100, verbose_name='Address Province')),
                ('candidate_party', models.CharField(db_index=True, max_length=255, unique=True, verbose_name='Pary Name')),
                ('candidate_position', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='Title')),
                ('candidate_position_number_of_slots', models.PositiveSmallIntegerField(verbose_name='Number of Slot')),
                ('election_name', models.CharField(db_index=True, max_length=255)),
                ('election_school_year', models.CharField(db_index=True, max_length=20, verbose_name='School Year')),
                ('election_day_from', models.DateField(db_index=True, verbose_name='Election Start Date')),
                ('election_day_to', models.DateField(db_index=True, verbose_name='Election End Date')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]