from django.db import models
from registration.models_base import BaseModel
# from registration.models import Election
from django.db.models import Count
import uuid
# Create your models here.

class DenormalizedVotesManager(models.Manager):
    '''
        Return report data
    '''

    def get_votes_distribution(self, election_id, distribution_by):
        if distribution_by == "voter_class_section":
            return super().get_queryset().filter(election_id=election_id).values(
                    'candidate_position',
                    'candidate_name',
                    'voter_class_grade_level',
                    'voter_class_section',
                    'candidate_position_priority'
                ).annotate(
                    votes=Count('candidate_name')
                ).order_by('candidate_position_priority','candidate_name','voter_class_grade_level','voter_class_section')
        else:
            return super().get_queryset().filter(election_id=election_id).values(
                    'candidate_position',
                    'candidate_name',
                    distribution_by,
                    'candidate_position_priority'
                ).annotate(
                    votes=Count('candidate_name')
                ).order_by('candidate_position_priority','candidate_name',distribution_by)

    def get_votes_per_candidate(self, election_id):
        return  super().get_queryset().filter(election_id=election_id).values(
                        'candidate_position',
                        'candidate_name',
                        'candidate_position_priority').annotate(
                            votes=Count('candidate_name')
                            ).order_by('candidate_position_priority','-votes')

class DenormalizedVotes(BaseModel):
    '''
        Denormalized table for reporting queries
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
    candidate_position_priority = models.PositiveSmallIntegerField(
                verbose_name="Priority",
                blank=False,
                null=False,
                default = 0,
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

    objects = DenormalizedVotesManager()

class WinnerCandidateDenormalized(BaseModel):
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
    candidate_position_priority = models.PositiveSmallIntegerField(
                verbose_name="Priority",
                blank=False,
                null=False,
                default = 0,
                db_index=True
    )
    number_of_votes =  models.PositiveIntegerField(
            null=False,
            blank=False,
            default=0,
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
    tie = models.BooleanField(
                default=False,
                verbose_name="Is Tie?"
    )

    class Meta:
        ordering = ('candidate_position_priority',)

    def __str__(self):
        return "{} ({})".format(self.candidate_name, self.candidate_position)

class ParticipationRate(BaseModel):
    GROUP_CHOICES = (
        ('OVERALL', 'OVERALL'),
        ('GRADE_LEVEL','GRADE_LEVEL'),
        ('SECTION','SECTION'),
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
    group = models.CharField(
            max_length = 20,
            choices = GROUP_CHOICES,
    )
    group_value = models.CharField(
            max_length=255,
            blank=False,
            null=False,
            db_index=True
    )
    total_voters = models.PositiveIntegerField(
            null=False,
            blank=False,
            db_index=True
    )
    total_casted_votes = models.PositiveIntegerField(
            null=False,
            blank=False,
            db_index=True
    )
    percentage = models.FloatField()

    class Meta:
        ordering = ('-election_day_to','group_value')

    @property
    def percentage_format(self):
        return round(self.percentage * 100, 2)

    @property
    def total_not_voted(self):
        return self.total_voters - self.total_casted_votes
