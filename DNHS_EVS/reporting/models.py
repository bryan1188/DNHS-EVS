from django.db import models
from registration.models_base import BaseModel
import uuid
# Create your models here.

class DenomarmalizedVotes(BaseModel):
    '''
        Denomarlized table for reporting queries
        This model should be heavily indexed for select optimization
    '''
    voter_id_h = models.CharField(
            max_length=255,
            verbose_name="Hashed Voter ID",
            null=False,
            default=uuid.uuid4().hex,
            unique=False,
    )
    voter_sex = models.CharField(
            max_length=1,
            verbose_name="Sex",
            db_index=True
    )
    voter_age = models.PositiveSmallIntegerField(
            verbose_name="Age",
            blank=True,
            null=True,
            db_index=True
    )
    voter_mother_tongue = models.CharField(max_length=50,
            verbose_name="Mother Tongue",
            db_index=True
    )
    voter_ethnic_group = models.CharField(
            max_length=50,
            verbose_name="Ethnic Group",
            db_index=True
    )
    voter_religion = models.CharField(
            max_length=100,
            verbose_name="Religion",
            db_index=True
    )
    voter_address_barangay = models.CharField(
            max_length=50,
            verbose_name="Address Barangay",
            db_index=True
    )
    voter_address_municipality = models.CharField(
            max_length=100,
            verbose_name="Address Municipality",
            db_index=True
    )
    voter_address_province = models.CharField(
            max_length=100,
            verbose_name="Address Province",
            db_index=True
    )
    voter_class_grade_level = models.CharField(
            max_length=20,
            verbose_name="Grade Level",
            null=True,
            db_index=True
    )
    voter_class_section = models.CharField(
            max_length=20,
            verbose_name="Section",
            null=True,
            db_index=True
    )
    candidate_name = models.CharField(
            max_length=255,
            verbose_name="Candidate Name",
            null=True,
            db_index=True
    )
    candidate_sex = models.CharField(
            max_length=1,
            verbose_name="Sex",
            db_index=True
    )
    candidate_age = models.PositiveSmallIntegerField(
            verbose_name="Age",
            blank=True,
            null=True,
            db_index= True
    )
    candidate_mother_tongue = models.CharField(max_length=50,
            verbose_name="Mother Tongue",
            db_index=True
    )
    candidate_ethnic_group = models.CharField(
            max_length=50,
            verbose_name="Ethnic Group",
            db_index=True
    )
    candidate_religion = models.CharField(
            max_length=100,
            verbose_name="Religion",
            db_index=True
    )
    candidate_address_barangay = models.CharField(
            max_length=50,
            verbose_name="Address Barangay",
            db_index=True
    )
    candidate_address_municipality = models.CharField(
            max_length=100,
            verbose_name="Address Municipality",
            db_index=True
    )
    candidate_address_province = models.CharField(
            max_length=100,
            verbose_name="Address Province",
            db_index=True
    )
    candidate_class_grade_level = models.CharField(
            max_length=20,
            verbose_name="Grade Level",
            null=True,
            db_index=True
    )
    candidate_class_section = models.CharField(
            max_length=20,
            verbose_name="Section",
            null=True,
            db_index=True
    )
    candidate_party = models.CharField(
            max_length=255,
            null=False,
            blank=False,
            unique=False,
            verbose_name="Pary Name",
            db_index=True
    )
    candidate_position = models.CharField(
            max_length=100,
            verbose_name="Title",
            null=False,
            blank=False,
            unique=False,
            db_index= True
    )
    candidate_position_number_of_slots = models.PositiveSmallIntegerField(
            verbose_name="Number of Slot",
            blank=False,
            null=False,
    )
    election_id = models.PositiveIntegerField(
            null=False,
            blank=False,
            db_index=True
    )
    election_name = models.CharField(
            max_length=255,
            blank=False,
            null=False,
            db_index=True
    )
    election_school_year = models.CharField(
            max_length=20,
            null=False,
            blank=False,
            verbose_name="School Year",
            db_index=True
    )
    election_day_from = models.DateField(
            null=False,
            blank=False,
            verbose_name="Election Start Date",
            db_index=True
    )
    election_day_to = models.DateField(
            null=False,
            blank=False,
            verbose_name="Election End Date",
            db_index=True
    )
