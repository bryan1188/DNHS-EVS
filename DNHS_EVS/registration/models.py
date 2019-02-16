from django.db import models

# Create your models here.
class School(models.Model):
    school_id = models.CharField(max_length=10, verbose_name="School ID", default="")
    name = models.CharField(max_length=50, verbose_name="School Name", default="")
    region = models.CharField(max_length=20, verbose_name="Region", default="")
    division = models.CharField(max_length=50, verbose_name="Division", default="")
    principal_name = models.CharField(max_length=150, verbose_name="Principal Name", default="")

    def __str__(self):
        return self.name

class Class(models.Model):
    school = models.ForeignKey(School, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="School")
    school_year = models.CharField(max_length=15, verbose_name="School Year")
    grade_level = models.CharField(max_length=20, verbose_name="Grade Level")
    section = models.CharField(max_length=20, verbose_name="Section")
    registered_male_bosy = models.PositiveSmallIntegerField(verbose_name="Registered Male BoSY", null=True)
    registered_female_bosy = models.PositiveSmallIntegerField(verbose_name="Registered Female BoSY", null=True)
    registered_total_bosy = models.PositiveSmallIntegerField(verbose_name="Registered Total BoSY", null=True)
    registered_male_eosy = models.PositiveSmallIntegerField(verbose_name="Registered Male EoSY", null=True)
    registered_female_eosy = models.PositiveSmallIntegerField(verbose_name="Registered Female EoSY", null=True)
    registered_total_bosy = models.PositiveSmallIntegerField(verbose_name="Registered Total EoSY", null=True)

    def __str__(self):
        return serlf.grade_level + " - " + self.section


#lookup tables for Student Table
class Sex(models.Model):
    sex = models.CharField(max_length=1,verbose_name="Sex")

    def __str__(self):
        return self.sex

class MotherTounge(models.Model):
    mother_tounge = models.CharField(max_length=50, verbose_name="Mother Tounge")

    def __str__(self):
        return self.mother_tounge

class EthnicGroup(models.Model):
    ethnic_group = models.CharField(max_length=50, verbose_name="Ethnic Group")

    def __str__(self):
        return self.ethnic_group

class Religion(models.Model):
    religion = models.CharField(max_length=100, verbose_name="Religion")

    def __str__(self):
        return self.religion

class AddressBarangay(models.Model):
    address_barangay = models.CharField(max_length=50, verbose_name="Address Barangay")

    def __str__(self):
        return self.address_barangay

class AddressMunicipality(models.Model):
    address_municipality = models.CharField(max_length=100, verbose_name="Address Municipality")

    def __str__(self):
        return self.address_municipality

class AddressProvince(models.Model):
    address_province = models.CharField(max_length=100, verbose_name="Address Province")

    def __str__(self):
        return self.address_province

#end of lookup tables for Student Table

class Student(models.Model):
    lrn = models.CharField(max_length=20, verbose_name="Learner Reference Number", unique=True)
    last_name = models.CharField(max_length=50, verbose_name="Last Name", null=True)
    first_name = models.CharField(max_length=50, verbose_name="First Name", null=True)
    middle_name = models.CharField(max_length=50, verbose_name="Middle Name", null=True, blank=True)
    sex = models.ForeignKey(Sex, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Sex")
    birth_date = models.DateField(verbose_name="Birth Date", blank=True, null=True)
    age = models.PositiveSmallIntegerField(verbose_name="Age", blank=True, null=True)
    mother_tounge = models.ForeignKey(MotherTounge, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Mother Tounge")
    ethnic_group = models.ForeignKey(EthnicGroup, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Ethnic Group")
    religion = models.ForeignKey(Religion, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Religion")
    address_house_no = models.CharField(max_length=50,verbose_name="Address House Number",blank=True, null=True)
    address_barangay = models.ForeignKey(AddressBarangay, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Address Barangay")
    address_municipality = models.ForeignKey(AddressMunicipality, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Address Municipality")
    address_province = models.ForeignKey(AddressProvince, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Address Province")
    father_name = models.CharField(max_length=150, null=True, verbose_name="Father's Name", blank=True)
    mother_name = models.CharField(max_length=150, null=True, verbose_name="Mother's Name", blank=True)
    guardian_name = models.CharField(max_length=150, null=True, verbose_name="Guardian's Name", blank=True)
    guardian_relationship = models.CharField(max_length=50, null=True, verbose_name="Guardian Relationship", blank=True)
    parent_guardian_contact_no = models.CharField(max_length=50, null=True, verbose_name="Parent Guardian Contact Number", blank=True)
    remarks = models.CharField(max_length=255, null=True, verbose_name="Remarks", blank=True)

    def __str__(self):
        if (self.middle_name != ""):
            return self.first_name + ", " + self.last_name + ", " + self.middle_name[:1].upper() + "."
        else:
            return self.first_name + ", " + self.last_name + ", "

class ElectionOfficer(models.Model):
    ACTIVE_CHOICES = (
        ('Y','Active'),
        ('N','Inactive')
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Student")
    active_flag = models.CharField(max_length=1, choices=ACTIVE_CHOICES, verbose_name="Active Flag Identifier")

    def __str__(self):
        return self.student

    @property
    def is_active(self): #use to identify if election officer is currently active or not
        if (self.active_flag == 'Y'):
            return True
        else:
            return False
