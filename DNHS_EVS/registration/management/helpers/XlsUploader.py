import xlrd
from django.utils.six.moves import range
from registration import models
from registration.management.helpers.import_helpers import XlsImportHelper
import datetime

class XlsUploader(XlsImportHelper):
        # school_data = {}
        # class_data = {}
        # my_helper = ""

        def __init__(self, *args, **kwargs):
            super(XlsUploader,self).__init__(*args, **kwargs)
            self._school_data = None
            self._class_data = None
            self._my_helper = XlsImportHelper(sheet=self._sheet)
            self._class_object = None
            self._student_list =  []

        #column properties
        @property
        def LRN_column(self, *args, **kwargs):
            return self.my_helper.getRowColumnNo(search_string='lrn',wild_search=False)[1]

        @property
        def student_name_column(self, *args, **kwargs):
            return self.my_helper.getRowColumnNo(search_string="name\n(last name,")[1]

        @property
        def sex_column(self,*args,**kwargs):
            return self.my_helper.getRowColumnNo(search_string="sex (m/f")[1]

        @property
        def birth_date_column(self,*args,**kwargs):
            return self.my_helper.getRowColumnNo(search_string="birth date")[1]

        @property
        def age_column(self,*args,**kwargs):
            return self.my_helper.getRowColumnNo(search_string="age as of")[1]

        @property
        def mother_tongue_column(self,*args,**kwargs):
            return self.my_helper.getRowColumnNo(search_string="mother tong")[1]

        @property
        def ethnic_group_column(self,*args,**kwargs):
            return self.my_helper.getRowColumnNo(search_string="ethnic group")[1]

        @property
        def religion_column(self,*args,**kwargs):
            return self.my_helper.getRowColumnNo(search_string="religion")[1]

        @property
        def house_no_column(self,*args,**kwargs):
            return self.my_helper.getRowColumnNo(search_string="house #")[1]

        @property
        def barangay_column(self,*args,**kwargs):
            return self.my_helper.getRowColumnNo(search_string="barangay")[1]

        @property
        def municipality_city_column(self,*args,**kwargs):
            return self.my_helper.getRowColumnNo(search_string="municipality")[1]

        @property
        def province_column(self,*args,**kwargs):
            return self.my_helper.getRowColumnNo(search_string="province")[1]

        @property
        def father_name_column(self,*args,**kwargs):
            return self.my_helper.getRowColumnNo(search_string="father's name")[1]

        @property
        def mother_name_column(self,*args,**kwargs):
            return self.my_helper.getRowColumnNo(search_string="mother's maiden")[1]

        @property
        def guardian_name_column(self,*args,**kwargs):
            return self.my_helper.getRowColumnNo(search_string="name", wild_search=False)[1]

        @property
        def guardian_relationship_column(self,*args,**kwargs):
            return self.my_helper.getRowColumnNo(search_string="relationship")[1]

        @property
        def parent_guardian_contact_no_column(self,*args,**kwargs):
            return self.my_helper.getRowColumnNo(search_string="contact number")[1]

        @property
        def remarks_column(self,*args,**kwargs):
            return self.my_helper.getRowColumnNo(search_string="remarks", wild_search=False)[1]
        #end of column column properties

        @property
        def my_helper(self):
            return self._my_helper

        #Table properties. Properties that represent a Table in the database
        @property
        def school_data(self, *args, **kwargs):
            school_id_region = self.my_helper.getSchoolIDRegionValue()
            self._school_data = {
                'school_id': school_id_region.get('school_id'),
                'name': self.my_helper.getValueHorizontalAdjacent(search_string='School Name'),
                'region': school_id_region.get('region'),
                'division': self.my_helper.getValueHorizontalAdjacent(search_string='division'),
                'principal_name': self.my_helper.getValueVerticalAdjacent(search_string='school head')
            }
            return self._school_data

        @property
        def class_data(self, *args, **kwargs):
            bosy_data = self.my_helper.getBoSY()
            eosy_data = self.my_helper.getEoSY()
            self._class_data = {
                'school_year': self.my_helper.getValueHorizontalAdjacent(search_string='school year'),
                'grade_level': self.my_helper.getValueHorizontalAdjacent(search_string='grade level').split("(")[0].strip(), #to trim the unwanted characters after (
                'section': self.my_helper.getValueHorizontalAdjacent(search_string='section'),
                'registered_male_bosy':  self.helper_convertIntor0(string=bosy_data.get('male',0)),
                'registered_female_bosy':  self.helper_convertIntor0(string=bosy_data.get('female',0)),
                'registered_total_bosy':  self.helper_convertIntor0(string=bosy_data.get('total',0)),
                'registered_male_eosy':  self.helper_convertIntor0(string=eosy_data.get('male',0)),
                'registered_female_eosy':  self.helper_convertIntor0(string=eosy_data.get('female',0)),
                'registered_total_eosy':  self.helper_convertIntor0(string=eosy_data.get('total',0)),
                'adviser': self.my_helper.getValueVerticalAdjacent(search_string='adviser'),
            }
            return self._class_data

        #end of Table properties

        @property
        def class_object(self, *args, **kwargs):
            if self._class_object is None: #if empty, then upload class to create class object
                self._class_object = self.uploadClass()
            return self._class_object

        @property
        def student_list(self, *args, **kwargs):
            return self._student_list

        #self helper methods
        def helper_convertIntor0(self, *args, **kwargs):
            return int(kwargs.get('string')) if kwargs.get('string') else 0 #if string is blank return zero

        def helper_setAttributes(self, *args, **kwargs):
            """
                helpter method that set attributes to a certain objects, mostly model object.
                parameters: object(model), attributes(dictionary)
            """
            for attribute, value in kwargs.get('attributes').items():
                setattr(kwargs.get('object'), attribute, value)
            return kwargs.get('object')

        #end of self helper methods

        def uploadAllData(self, *args, **kwargs):
            self.uploadClass()
            self.uploadStudent()

        def uploadSchool(self, *args, **kwargs):
            school, created = models.School.objects.get_or_create(
                school_id = self.my_helper.getSchoolIDRegionValue().get('school_id'),
                school_year = self.my_helper.getValueHorizontalAdjacent(search_string='school year'),
            )
            school = self.helper_setAttributes(object=school, attributes=self.school_data)
            school.save()
            return school

        def uploadClass(self, *args, **kwargs):
            class_object, created = models.Class.objects.get_or_create( #primary keys
                school =  self.uploadSchool(),
                school_year = self.class_data.get('school_year'),
                grade_level = self.class_data.get('grade_level'),
                section = self.class_data.get('section'),
            )
            class_object =  self.helper_setAttributes(object=class_object, attributes=self.class_data)
            class_object.save()
            return class_object

        def uploadStudent(self, *args, **kwargs):
            """
                iterate on every row and upload the student record if not exist.
                If record exist based on student LRN, then do an update
            """
            #iterate on all rows of the sheet
            for rownum in range(self._sheet.nrows): #check on every row
                #check if row is valid student data
                if self._sheet.row_values(rownum)[self.LRN_column].__str__().strip().isdigit() and len(self._sheet.row_values(rownum)[self.LRN_column].__str__().strip()) > 4:
                    #get the data and put in the dictionary
                    student_data = {}
                    if len(self._sheet.row_values(rownum)[self.student_name_column].__str__().strip().split(',')) > 2 : #middle name available
                        student_data = {
                            'last_name': self._sheet.row_values(rownum)[self.student_name_column].__str__().strip().split(',')[0].strip(),
                            'first_name': self._sheet.row_values(rownum)[self.student_name_column].__str__().strip().split(',')[1].strip(),
                            'middle_name': self._sheet.row_values(rownum)[self.student_name_column].__str__().strip().split(',')[2].strip()
                        }
                    else:
                        student_data = {
                            'last_name': self._sheet.row_values(rownum)[self.student_name_column].__str__().strip().split(',')[0].strip(),
                            'first_name': self._sheet.row_values(rownum)[self.student_name_column].__str__().strip().split(',')[1].strip(),
                        }

                    student_data.update({
                        'sex': models.Sex.objects.get_or_create(sex=self._sheet.row_values(rownum)[self.sex_column].__str__().strip()[:1].upper())[0], #get the index 0 from the tupple (object, created)
                        'birth_date': datetime.datetime.strptime(self._sheet.row_values(rownum)[self.birth_date_column].__str__().strip(), '%m-%d-%Y').date(),
                        'age': self.helper_convertIntor0(string=self._sheet.row_values(rownum)[self.age_column].__str__().strip()),
                        'mother_tongue': models.MotherTongue.objects.get_or_create(mother_tongue=self._sheet.row_values(rownum)[self.mother_tongue_column].__str__().strip())[0],
                        'ethnic_group': models.EthnicGroup.objects.get_or_create(ethnic_group=self._sheet.row_values(rownum)[self.ethnic_group_column].__str__().strip())[0],
                        'religion':  models.Religion.objects.get_or_create(religion=self._sheet.row_values(rownum)[self.religion_column].__str__().strip())[0],
                        'address_house_no': self._sheet.row_values(rownum)[self.house_no_column].__str__().strip(),
                        'address_barangay': models.AddressBarangay.objects.get_or_create(address_barangay=self._sheet.row_values(rownum)[self.barangay_column].__str__().strip())[0],
                        'address_municipality': models.AddressMunicipality.objects.get_or_create(address_municipality=self._sheet.row_values(rownum)[self.municipality_city_column].__str__().strip())[0],
                        'address_province': models.AddressProvince.objects.get_or_create(address_province=self._sheet.row_values(rownum)[self.province_column].__str__().strip())[0],
                        'father_name': self._sheet.row_values(rownum)[self.father_name_column].__str__().strip(),
                        'mother_name': self._sheet.row_values(rownum)[self.mother_name_column].__str__().strip(),
                        'guardian_name': self._sheet.row_values(rownum)[self.guardian_name_column].__str__().strip(),
                        'guardian_relationship': self._sheet.row_values(rownum)[self.guardian_relationship_column].__str__().strip(),
                        'parent_guardian_contact_no': self._sheet.row_values(rownum)[self.parent_guardian_contact_no_column].__str__().strip(),
                        'remarks': self._sheet.row_values(rownum)[self.remarks_column].__str__().strip(),
                    })

                    #check if student already exist, if not then create, if exist update
                    student, created = models.Student.objects.get_or_create(lrn=self._sheet.row_values(rownum)[self.LRN_column].__str__().strip())
                    student =  self.helper_setAttributes(object=student, attributes=student_data)
                    student.save()
                    student.classes.add(self.class_object)#populate many to many bridge table
                    self._student_list.append(student.id)
