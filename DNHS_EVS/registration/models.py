from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BaseModel(models.Model): #base model for all my models. This will have the column create_date, last_update_date, Created_by, last_updated_by
    created_date = models.DateTimeField(
                auto_now_add=True,
                null=True
    )
    modified_date = models.DateTimeField(
                auto_now=True,
                null=True
    )

    class Meta:
        abstract = True

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
    school_year = models.CharField(max_length=15, verbose_name="School Year", null=True)
    grade_level = models.CharField(max_length=20, verbose_name="Grade Level", null=True)
    section = models.CharField(max_length=20, verbose_name="Section", null=True)
    registered_male_bosy = models.PositiveSmallIntegerField(verbose_name="Registered Male BoSY", null=True)
    registered_female_bosy = models.PositiveSmallIntegerField(verbose_name="Registered Female BoSY", null=True)
    registered_total_bosy = models.PositiveSmallIntegerField(verbose_name="Registered Total BoSY", null=True)
    registered_male_eosy = models.PositiveSmallIntegerField(verbose_name="Registered Male EoSY", null=True)
    registered_female_eosy = models.PositiveSmallIntegerField(verbose_name="Registered Female EoSY", null=True)
    registered_total_eosy = models.PositiveSmallIntegerField(verbose_name="Registered Total EoSY", null=True)
    adviser = models.CharField(max_length=150, verbose_name='Adviser', null=True)

    class Meta:
        unique_together = (('school_year', 'grade_level','section'),)
        ordering = ('school_year', 'grade_level',
                    'section')

    def __str__(self):
        return self.grade_level + " - " + self.section + "(" + self.school_year + ")"

#lookup tables for Student Table

class SexManager(models.Manager):
    def get_by_natural_key(self, sex):
        return self.get(first_name=sex)

class Sex(BaseModel):
    sex = models.CharField(max_length=1,verbose_name="Sex")
    objects = SexManager()

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

#end of lookup tables for Student Table

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
                related_query_name='students'
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
                verbose_name=('classes'),
                blank=True,
    )

    class Meta:
        ordering = ('last_name', 'first_name',
                    'middle_name')

    def __str__(self):
        if (self.middle_name != ""):
            return self.last_name + ", " + self.first_name + " " + self.middle_name[:1].upper() + "."
        else:
            return self.last_name + ", " + self.first_name


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

class Election(BaseModel):
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
                related_name="created_by",
                related_query_name='elections created'
    )
    last_updated_by = models.ForeignKey(
                User,
                on_delete=models.SET_NULL,
                null=True,
                verbose_name="Last Updated by",
                related_name="updated_by",
                related_query_name='elections last updated'
    )

    class Meta:
        ordering = ('-school_year', '-election_day_from')
        unique_together = (('school_year', 'election_day_from','election_day_to'),)

    def __str__(self):
        return self.name + '(' + self.school_year  + ')'
