from django.db import models
from registration.models_election import Position
from django.contrib.auth.models import User
from registration.models_base import BaseModel
from election.models import Ballot
from election.management.helpers.hasher_helpers import MyHasher
from registration.management.helpers.token_generator import id_generator
# from reporting.management.helpers.denormalizer import denomarlized_election
import datetime
from django.conf import settings
import uuid
import hashlib
from django.utils import timezone


#Model Managers###############################################
class ObjectManagerActive(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active = True)

    def get_candidate_of_voter(self, election, grade_level):
        '''
            Given an election and grade level, it will return a list of candidate
            Will be used in generating a list of candidate per student
            Use in Candidate model
        '''
        return super().get_queryset().all().filter(
                election = election,
                position__grade_levels__grade_level = grade_level
        )

    def is_election_day(self):
        '''
            return True if current date is in range of any election that has status
                of 'FINALIZED'
            Used in Election Model
        '''
        date_now = datetime.datetime.now().date()
        if super().get_queryset().filter(election_day_to__gte=date_now,
            election_day_from__lte=date_now, status='FINALIZED').exists():
            return True
        else:
             return False

    def get_current_election(self):
        '''
            get the current election and return the election instance
            used in Election Model
            used in election.viewsF.vote.authenticate_voter_ajax
        '''
        date_now = datetime.datetime.now().date()
        return super().get_queryset().filter(election_day_to__gte=date_now,
            election_day_from__lte=date_now, status='FINALIZED').first()

class ObjectManagerAll(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()

class ClassSchoolYearManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-school_year')\
        .values_list('school_year',flat=True).distinct()

class StudentManager(models.Manager):
    def get_by_natural_key(self, first_name, last_name):
        return "{}, {}".format(self.get(last_name=last_name), self.get(first_name=first_name))

class SexManager(models.Manager):
    def get_by_natural_key(self, sex):
        return self.get(sex=sex)

class VoteManger(models.Manager):
    '''
        For additional security, Vote should only return valid votes based on
            valid_vote propert.
    '''
    def get_queryset(self):
        votes = super().get_queryset()
        vote_ids = [vote.id for vote in votes if vote.valid_vote]
        return super().get_queryset().filter(id__in=vote_ids)

    def get_last_create_date(self):
        if super().get_queryset().all().count() > 1:
            return timezone.localtime(super().get_queryset().all().aggregate(
                                            models.Max('created_date')
                                            ).get('created_date__max')
                                        )
        else:
            return None

#end of Model Managers ########################################

class School(BaseModel):
    school_id = models.CharField(max_length=10, verbose_name="School ID", default="")
    school_year = models.CharField(max_length=15, verbose_name="School Year", null=True)
    name = models.CharField(max_length=50, verbose_name="School Name", default="")
    region = models.CharField(max_length=20, verbose_name="Region", default="")
    division = models.CharField(max_length=50, verbose_name="Division", default="")
    principal_name = models.CharField(max_length=150, verbose_name="Principal Name", default="")

    class Meta:
        unique_together = (('school_id', 'school_year'),)
    def __str__(self):
        return self.name

class Class(BaseModel):
    school = models.ForeignKey(School, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="School", related_name='classes')
    school_year = models.CharField(max_length=15, verbose_name="School Year", null=True, db_index= True)
    grade_level = models.CharField(max_length=20, verbose_name="Grade Level", null=True)
    section = models.CharField(max_length=20, verbose_name="Section", null=True)
    registered_male_bosy = models.PositiveSmallIntegerField(verbose_name="Registered Male BoSY", null=True)
    registered_female_bosy = models.PositiveSmallIntegerField(verbose_name="Registered Female BoSY", null=True)
    registered_total_bosy = models.PositiveSmallIntegerField(verbose_name="Registered Total BoSY", null=True)
    registered_male_eosy = models.PositiveSmallIntegerField(verbose_name="Registered Male EoSY", null=True)
    registered_female_eosy = models.PositiveSmallIntegerField(verbose_name="Registered Female EoSY", null=True)
    registered_total_eosy = models.PositiveSmallIntegerField(verbose_name="Registered Total EoSY", null=True)
    adviser = models.CharField(max_length=150, verbose_name='Adviser', null=True)
    objects = ObjectManagerAll()
    school_year_distinct = ClassSchoolYearManager()

    class Meta:
        unique_together = (('school_year', 'grade_level','section'),)
        ordering = ('school_year', 'grade_level',
                    'section')

    def __str__(self):
        return self.grade_level + " - " + self.section + "(" + self.school_year + ")"

    @property
    def grade_level_section(self):
        return self.grade_level + " - " + self.section

#lookup tables for Student Table################
class Sex(BaseModel):
    sex = models.CharField(max_length=1,verbose_name="Sex")
    # objects = SexManager()

    def natural_key(self):
        return (self.sex)

    def __str__(self):
        return self.sex

class MotherTongue(BaseModel):
    mother_tongue = models.CharField(max_length=50, verbose_name="Mother Tongue")

    def __str__(self):
        return self.mother_tongue

class EthnicGroup(BaseModel):
    ethnic_group = models.CharField(max_length=50, verbose_name="Ethnic Group")

    def __str__(self):
        return self.ethnic_group

class Religion(BaseModel):
    religion = models.CharField(max_length=100, verbose_name="Religion")

    def __str__(self):
        return self.religion

class AddressBarangay(BaseModel):
    address_barangay = models.CharField(max_length=50, verbose_name="Address Barangay")

    def __str__(self):
        return self.address_barangay

class AddressMunicipality(BaseModel):
    address_municipality = models.CharField(max_length=100, verbose_name="Address Municipality")

    def __str__(self):
        return self.address_municipality

class AddressProvince(BaseModel):
    address_province = models.CharField(max_length=100, verbose_name="Address Province")

    def __str__(self):
        return self.address_province
#end of lookup tables for Student Table#########

class Student(BaseModel):
    lrn = models.CharField(
                max_length=20,
                verbose_name="Learner Reference Number",
                unique=True,
                db_index= True
    )
    last_name = models.CharField(
                max_length=50,
                verbose_name="Last Name",
                null=True,
                db_index= True
    )
    first_name = models.CharField(
                max_length=50,
                verbose_name="First Name",
                null=True,
                db_index= True
    )
    middle_name = models.CharField(
                max_length=50,
                verbose_name="Middle Name",
                null=True,
                blank=True,
                db_index= True
    )
    sex = models.ForeignKey(
                Sex,
                on_delete=models.SET_NULL,
                blank=True,
                null=True,
                verbose_name="Sex",
                related_query_name='students',
                related_name = 'students'
    )
    birth_date = models.DateField(
                verbose_name="Birth Date",
                blank=True,
                null=True
    )
    age = models.PositiveSmallIntegerField(
                verbose_name="Age",
                blank=True,
                null=True
    )
    mother_tongue = models.ForeignKey(
                MotherTongue,
                on_delete=models.SET_NULL,
                blank=True,
                null=True,
                verbose_name="Mother Tongue",
                related_query_name='students'
    )
    ethnic_group = models.ForeignKey(
                EthnicGroup,
                on_delete=models.SET_NULL,
                blank=True,
                null=True,
                verbose_name="Ethnic Group",
                related_query_name='students'
    )
    religion = models.ForeignKey(
                Religion,
                on_delete=models.SET_NULL,
                blank=True,
                null=True,
                verbose_name="Religion",
                related_query_name='students'
    )
    address_house_no = models.CharField(
                max_length=50,
                verbose_name="Address House Number",
                blank=True,
                null=True
    )
    address_barangay = models.ForeignKey(
                AddressBarangay,
                on_delete=models.SET_NULL,
                blank=True,
                null=True,
                verbose_name="Address Barangay",
                related_query_name='students'
    )
    address_municipality = models.ForeignKey(
                AddressMunicipality,
                on_delete=models.SET_NULL,
                blank=True,
                null=True,
                verbose_name="Address Municipality",
                related_query_name='students'
    )
    address_province = models.ForeignKey(
                AddressProvince,
                on_delete=models.SET_NULL,
                blank=True,
                null=True,
                verbose_name="Address Province",
                related_query_name='students'
    )
    father_name = models.CharField(
                max_length=150,
                null=True,
                verbose_name="Father's Name",
                blank=True
    )
    mother_name = models.CharField(
                max_length=150, null=True,
                verbose_name="Mother's Name",
                blank=True
    )
    guardian_name = models.CharField(
                max_length=150,
                null=True,
                verbose_name="Guardian's Name",
                blank=True
    )
    guardian_relationship = models.CharField(
                max_length=50,
                null=True,
                verbose_name="Guardian Relationship",
                blank=True
    )
    parent_guardian_contact_no = models.CharField(
                max_length=50,
                null=True,
                verbose_name="Parent Guardian Contact Number",
                blank=True
    )
    remarks = models.CharField(
                max_length=255,
                null=True,
                verbose_name="Remarks",
                blank=True
    )
    classes = models.ManyToManyField(
                Class,
                verbose_name='classes',
                blank=True,
                related_name='students'
    )


    class Meta:
        ordering = ('last_name', 'first_name',
                    'middle_name')

    def __str__(self):
        if self.middle_name == "-" or not self.middle_name:
            return "{}, {}".format(self.last_name, self.first_name)
        else:
            return "{}, {} {}.".format(self.last_name,
                                        self.first_name,
                                        self.middle_name[:1].upper()
                                       )
        # if self.middle_name != "" or:
        #     return self.last_name + ", " + self.first_name + " " + self.middle_name[:1].upper() + "."
        # else:
        #     return self.last_name + ", " + self.first_name

    def natural_key(self):
        return self.__str__()

    @property
    def name_title(self):
        if self.middle_name == "-" or not self.middle_name:
            # middle name is blank or set to "-"
            return "{} {}".format(self.first_name,
                                    self.last_name
                                )
        else:
            return "{} {} {}".format(self.first_name,
                                    self.middle_name,
                                    self.last_name
                                    )


#related to users ##############################
class ElectionOfficer(BaseModel):
    #null True to update later. editable to map
    student = models.OneToOneField(Student, on_delete=models.CASCADE, verbose_name="Student", related_query_name='student')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User", related_query_name='user', null=False, primary_key=True)
    is_active = models.BooleanField(default=True, verbose_name="Is Active?")

    def __str__(self):
        return self.student

class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User", related_query_name='user', null=False, primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Student", related_query_name='students', null=True)
    password_is_temp = models.BooleanField(default=True, verbose_name="Password Is Temp?")
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, default='profile_pics/default_avatar.png')

    def __str__(self):
        return self.user.username
#end of related to users ########################


#related to election#############################
class Election(BaseModel):

    STATUS_CHOICES = (
        ('NEW', 'NEW'),
        ('FINALIZED','FINALIZED'),
        ('COMPLETED','COMPLETED'),
        ('CANCELED','CANCELED')
    )
    name = models.CharField(
                max_length=255,
                null=False,
                blank=False,
                verbose_name="Name",
    )
    school_year = models.CharField(
                max_length=20,
                null=False,
                blank=False,
                verbose_name="School Year",
    )
    description = models.CharField(
                max_length=500,
                null=True,
                blank=True,
                verbose_name="Description"
    )
    election_day_from = models.DateField(
                null=False,
                blank=False,
                verbose_name="Election Start Date"
    )
    election_day_to = models.DateField(
                null=False,
                blank=False,
                verbose_name="Election End Date"
    )
    created_by = models.ForeignKey(
                User,
                on_delete=models.SET_NULL,
                null=True,
                verbose_name="Created by",
                related_name="election_created_by",
                related_query_name='elections created'
    )
    last_updated_by = models.ForeignKey(
                User,
                on_delete=models.SET_NULL,
                null=True,
                verbose_name="Last Updated by",
                related_name="election_updated_by",
                related_query_name='elections last updated'
    )
    is_active = models.BooleanField(
            default=True,
            verbose_name="Is Active?"
    )
    positions = models.ManyToManyField(
            Position,
            verbose_name = 'Positions',
            blank = True,
            related_name = 'elections'
    )
    status = models.CharField(
            max_length = 20,
            choices = STATUS_CHOICES,
            default = 'NEW'
    )
    is_token_generated = models.BooleanField(
            default=False,
            verbose_name="Token Available?"
    )

    objects = ObjectManagerActive()

    all_objects = ObjectManagerAll()

    class Meta:
        ordering = ( '-election_day_from',)
        unique_together = (('school_year', 'election_day_from','election_day_to'),)

    def __str__(self):
        return self.name + '(' + self.school_year  + ')'

    def natural_key(self):
        return self.__str__()

    # do it in view. facing issue in importing classes. It got circular reference
    # def denormalized(self):
    #     '''
    #         Denormalized all votes for analysis.
    #         Denormalized table is optimized for select queries which is heavily
    #             used in reporting
    #         DenomarmalizedVotes model will be populated based on this election
    #         Returns True if success, False if something wrong
    #     '''
    #     return denomarlized_election(self)
    #
    # def complete_election(self):
    #     '''
    #         This will complete the election instance.
    #         Complete means winner should be declared and no votes will be accepted.
    #         Change the status to COMPLETED.
    #         Archive all votes of the electin instance
    #     '''
    #     pass

class Party(BaseModel):
    name = models.CharField(
                max_length=255,
                null=False,
                blank=False,
                unique=True,
                verbose_name="Name",
    )
    created_by = models.ForeignKey(
            User,
            on_delete=models.SET_NULL,
            null=True,
            verbose_name="Created by",
            related_name="party_created_by",
            related_query_name='elections created'
    )
    last_updated_by = models.ForeignKey(
            User,
            on_delete=models.SET_NULL,
            null=True,
            verbose_name="Last Updated by",
            related_name="party_updated_by",
            related_query_name='elections last updated'
    )
    is_active = models.BooleanField(
            default=True,
            verbose_name="Is Active?"
    )

    #overriding objects so that the actives will only show on the form that will consume this model
    #or any other form that call this model
    objects = ObjectManagerActive()

    all_objects = ObjectManagerAll()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.__str__()

class Candidate(BaseModel):
    student = models.ForeignKey(
            Student,
            on_delete = models.SET_NULL,
            blank = False,
            null = True,
            verbose_name = "Student",
            related_name = 'candidates'
    )
    party = models.ForeignKey(
            Party,
            on_delete = models.SET_NULL,
            blank = False,
            null = True,
            verbose_name = "Party",
            related_name = 'candidates'
    )
    election = models.ForeignKey(
            Election,
            on_delete = models.SET_NULL,
            blank = False,
            null = True,
            verbose_name = 'Election',
            related_name = 'candidates'
    )
    position = models.ForeignKey(
            Position,
            on_delete = models.SET_NULL,
            blank = False,
            null = True,
            verbose_name = 'Position',
            related_name = 'candidates'
    )
    created_by = models.ForeignKey(
            User,
            on_delete=models.SET_NULL,
            null=True,
            verbose_name="Created by",
            related_name="candidates_created",
            related_query_name='position_created'
    )
    last_updated_by = models.ForeignKey(
            User,
            on_delete=models.SET_NULL,
            null=True,
            verbose_name="Last Updated by",
            related_name="candidates_last_updated",
            related_query_name='position_last_updated'
    )
    is_active = models.BooleanField(
            default=True,
            verbose_name="Is Active?"
    )
    profile_pic = models.ImageField(
            upload_to='candidate_pics/',
            blank=True, default='candidate_pics/avatar.png')
    #overriding objects so that the actives will only show on the form that will consume this model
    #or any other form that call this model
    objects = ObjectManagerActive()

    all_objects = ObjectManagerAll()

    class Meta:
        unique_together = (('student', 'election'),)
        ordering = ('position', 'student',)

    def __str__(self):
        return self.student.__str__() + '(' + self.position.__str__() + ')'

    @property
    def candidate_class(self):
        return self.student.classes.filter(
                school_year=self.election.school_year
                ).first()

class Voter(BaseModel):
    student = models.ForeignKey(
            Student,
            on_delete = models.SET_NULL,
            blank = False,
            null = True,
            verbose_name = "Student",
            related_name = 'voters'
    )
    voter_token = models.CharField(
            max_length=50,
            verbose_name="Token",
            null=False,
            db_index=True
    )
    student_class =  models.ForeignKey(
            Class,
            on_delete = models.SET_NULL,
            blank = False,
            null = True,
            verbose_name = "Student Class",
            related_name = 'voters'
    )
    election = models.ForeignKey(
            Election,
            on_delete = models.SET_NULL,
            blank = False,
            null = True,
            verbose_name = "Election",
            related_name = 'voters'
    )
    candidates = models.ManyToManyField(
            Candidate,
            verbose_name = 'Candidates',
            blank = True,
            related_name = 'voters'
    )
    is_vote_casted = models.BooleanField(
            default=False,
            verbose_name="Vote casted?"
    )
    voter_token_for_validation_h = models.CharField(
            max_length=250,
            verbose_name="Vote Validation Token",
            null=True,
    )
    is_temporary_token = models.BooleanField(
            default=False,
            verbose_name="Temporary Token"
    )

    validation_token_hasher = MyHasher()
    validation_token_hasher.hasher_lib = settings.HASHLIB_VOTER_NEW_TOKEN

    def authenticate_for_vote_validation(self, validation_token):
        '''
            check if the voter enters the correct validation_token
        '''
        return self.validation_token_hasher.check(
                    self.voter_token_for_validation_h,
                    validation_token)

    def assign_voter_token_for_validation_h(self):
        '''
            update voter_token_for_validation_h and return the un-hashed generated token
        '''
        voter_validation_token = id_generator(
            6,
            "{}{}".format(self.student.lrn,self.student.__str__())
        )
        self.voter_token_for_validation_h = self.validation_token_hasher.hash(voter_validation_token)
        return voter_validation_token

    @property
    def hash_id(self):
        my_hasher = MyHasher()
        return my_hasher.hash_fixed_salt(
                            str(self.id) + settings.HASHING_SECRET_KEY
                        )

    @property
    def ballot(self):
        try:
            return Ballot.objects.get(
                    voter_id_h = self.hash_id
                    )
        except Ballot.DoesNotExist:
            return None


    class Meta:
        unique_together = (('student', 'election'),)

    def __str__(self):
        return self.student.__str__()

#end of related to election ########################


# models related to voting ##################
class Vote(BaseModel):
    '''
        Minimized index in this model for performance optimization
    '''
    hashed_id = models.CharField(
            max_length=255,
            null=False,
            default=uuid.uuid4().hex,
            unique=True
    )
    ballot = models.ForeignKey(
            Ballot,
            on_delete = models.SET_NULL,
            blank = False,
            null = True,
            verbose_name = "Ballot",
            related_name = 'votes'
    )
    candidate = models.ForeignKey(
            Candidate,
            on_delete = models.SET_NULL,
            blank = False,
            null = True,
            verbose_name = "Candidate",
            related_name = 'votes'
    )

    class Meta:
        unique_together = (('ballot', 'candidate'),)

    hasher = MyHasher()
    # used sha512 for better security
    hasher.hasher_lib = hashlib.sha512

    # if settings.VOTE_SECURITY: #check if VOTE SECURITY is enabled
        #for additional security, only return valid vote
    objects = VoteManger() #Security is enforced. not an option

    def populate_hashed_id(self):
        # add mechanism to check if hash generated already exist.
        self.hashed_id = self.hasher.hash(self.ballot.voter_id_h
                            + settings.HASHING_SECRET_KEY)

    @property
    def valid_vote(self):
        '''
            these are the additional security for vote model
            check if a certain vote is valid based on the hashed_id
            the application has no update privilege so it can't update the
                recored once inserted
            the application has no delete privilege so it can't delete any
                vote from a certain candidate
            once vote is casted, no update or delete needed

        '''
        try:
            return self.hasher.check(self.hashed_id, self.ballot.voter_id_h
                            + settings.HASHING_SECRET_KEY)
        except:
            return False

class VoteArchived(BaseModel):
    '''
        To improve voting experience, Vote model should be truncated every election.
        This is the archive table for Vote Model.
        Relationship should be maintain here when voter validate his/her vote
    '''
    hashed_id = models.CharField(
            max_length=255,
            null=False,
            default=uuid.uuid4().hex,
            unique=True
    )
    ballot = models.ForeignKey(
            Ballot,
            on_delete = models.SET_NULL,
            blank = False,
            null = True,
            verbose_name = "Ballot",
            related_name = 'votes_archived'
    )
    candidate = models.ForeignKey(
            Candidate,
            on_delete = models.SET_NULL,
            blank = False,
            null = True,
            verbose_name = "Candidate",
            related_name = 'votes_archived'
    )
    election = models.ForeignKey(
            Election,
            on_delete = models.SET_NULL,
            blank = False,
            null = True,
            verbose_name = "Election",
            related_name = 'votes_archived'
    )

    class Meta:
        unique_together = (('ballot', 'candidate'),)

    @property
    def valid_vote(self):
        '''
            these are the additional security for vote model
            check if a certain vote is valid based on the hashed_id
            the application has no update privilege so it can't update the
                recored once inserted
            the application has no delete privilege so it can't delete any
                vote from a certain candidate
            once vote is casted, no update or delete needed

        '''
        try:
            return self.hasher.check(self.hashed_id, self.ballot.voter_id_h
                            + settings.HASHING_SECRET_KEY)
        except:
            return False

# class WinnerCandidate(BaseModel):
#   denormalized this model. refer to reporting.models.WinnerCandidateDenormalized
#     election = models.ForeignKey(
#             Election,
#             on_delete = models.SET_NULL,
#             blank = False,
#             null = True,
#             verbose_name = 'Election',
#             related_name = 'winner_candidates'
#     )
#     candidate = models.ForeignKey(
#             Candidate,
#             on_delete = models.SET_NULL,
#             blank = False,
#             null = True,
#             verbose_name = 'Candidate',
#             related_name = 'winner_candidates'
#     )
#     tie = models.BooleanField(
#             default=False,
#             verbose_name="Is Tie?"
#     )
    # number_of_votes =  models.PositiveIntegerField(
    #         null=False,
    #         blank=False,
    #         default=0,
    #
    # )
    # candidate_position_priority

#end of related to voting ########################
