from django import forms
from registration.models import (Student,UserProfile,
                            Class,ElectionOfficer,Election,Party,Candidate)
from registration.models_election import Position
from django.contrib.auth.models import User,Group
from django.db.models import Q
from searchableselect.widgets import SearchableSelect


class UploadStudentsForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    # file_field = forms.FileField(widget=forms.ClearableFileInput())

class UserForm(forms.ModelForm):
    FOR_STUDENT_CHOICES = (
        ('election_officer','Election Officer'),
        ('candidate','Candidate')
    )
    FOR_OTHER_GROUPS_CHOICES = (
        ('teacher','Teacher'),
        ('system_administrator','System Administrator')
    )
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    for_student = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                      choices=FOR_STUDENT_CHOICES, required=False)
    student_lrn = forms.CharField(widget=forms.HiddenInput(), required=False,)
    other_groups = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                      choices=FOR_OTHER_GROUPS_CHOICES, required=False)

    class Meta:
        model = User
        fields = ('username','password','confirm_password','last_name','first_name')

    def clean_username(self):
        cleaned_data = super(UserForm, self).clean()
        username = cleaned_data['username']
        if self.instance.pk == None: #for insert
            if User.objects.filter(username__iexact=username).exists():
                raise forms.ValidationError(
                    username + " is already taken. Please use another username"
                )
        return username

    def clean_confirm_password(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError(
                "password and Confirm Password does not match"
            )
        return confirm_password

    def my_check_student_in_election_officer(self, student_lrn):
        student = Student.objects.filter(lrn__iexact=student_lrn).first()
        election_officer = ElectionOfficer.objects.filter(student=student).first()
        if election_officer:
            raise forms.ValidationError(
                "The selected student is already an election officer with a username " + str(election_officer.user) + ". Select another student"
            )

    def clean_student_lrn(self):
        cleaned_data = super().clean()
        for_student = cleaned_data['for_student']
        student_lrn = cleaned_data['student_lrn']
        if self.instance.pk == None: #for insert
            if 'election_officer' in for_student: #election officer is checked
                if  not student_lrn: #but student is not selected
                    raise forms.ValidationError(
                        "Please select Student"
                    )
                else: #lrn selected but check if the student is already an election officer
                    self.my_check_student_in_election_officer(student_lrn)
        else: #for update
            #need to check user that is not election officer yet but if mapped to student
            #that is election_officer already, raise an error
            self.my_check_student_in_election_officer(student_lrn)
        return student_lrn

class UserFormUpdate(forms.ModelForm):

    FOR_STUDENT_CHOICES = (
        ('election_officer','Election Officer'),
        ('candidate','Candidate')
    )
    FOR_OTHER_GROUPS_CHOICES = (
        ('teacher','Teacher'),
        ('system_administrator','System Administrator')
    )
    for_student = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                      choices=FOR_STUDENT_CHOICES, required=False)
    student_lrn = forms.CharField(widget=forms.HiddenInput(), required=False,)
    other_groups = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                      choices=FOR_OTHER_GROUPS_CHOICES, required=False)
    class Meta:
        model = User
        fields = ('username','last_name','first_name')

    def clean_username(self):
        cleaned_data = super().clean()
        username = cleaned_data['username']
        if self.instance.pk == None: #for insert
            if User.objects.filter(username__iexact=username).exists():
                raise forms.ValidationError(
                    username + " is already taken. Please use another username"
                )
        return username

    def my_check_student_in_election_officer(self, student_lrn):
        student = Student.objects.filter(lrn__iexact=student_lrn).first()
        election_officer = ElectionOfficer.objects.filter(student=student).first()
        if election_officer:
            raise forms.ValidationError(
                "The selected student is already an election officer with a username " + str(election_officer.user) + ". Select another student"
            )

    def clean_student_lrn(self):
        cleaned_data = super().clean()
        for_student = cleaned_data['for_student']
        student_lrn = cleaned_data['student_lrn']
        if self.instance.pk == None: #for insert
            if 'election_officer' in for_student: #election officer is checked
                if  not student_lrn: #but student is not selected
                    raise forms.ValidationError(
                        "Please select Student"
                    )
                else: #lrn selected but check if the student is already an election officer
                    self.my_check_student_in_election_officer(student_lrn)
        else: #for update
            #need to check user that is not election officer yet but if mapped to student
            #that is election_officer already, raise an error
            self.my_check_student_in_election_officer(student_lrn)
        return student_lrn

class UserFormUpdatePassword(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('password',)

    def clean_confirm_password(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError(
                "password and Confirm Password does not match"
            )
        return confirm_password

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_pic',)

class ClassFilterForm(forms.Form):
    school_year_list = Class.objects.all().order_by('school_year')\
                        .values_list('school_year',flat=True).distinct()
    school_year = forms.ModelChoiceField(
                queryset=school_year_list,
                widget = forms.Select(
                    attrs = {
                        'data-toggle': 'tooltip',
                        'data-placement': 'right',
                        'title': 'Apply filter by school year'
                        }
                )
                )
    grade_level = forms.ChoiceField(widget = forms.Select(
                attrs = {
                    #removed, got crazy whene applying selectpicker
                    # 'data-toggle': 'tooltip',
                    # 'data-placement': 'right',
                    # 'title': 'Apply filter by grade level',
                    }
    ))
    section =  forms.ChoiceField(widget = forms.Select(
                attrs = {
                    #removed, got crazy whene applying selectpicker
                    # 'data-toggle': 'tooltip',
                    # 'data-placement': 'right',
                    # 'title': 'Apply filter by section'
                    },
                    # initial = '---------'
    ))

class UserFilterForm(forms.Form):
    queryset_ =  Group.objects.all().order_by('name').values_list('name', flat=True).distinct()
    group = forms.ModelChoiceField(widget=forms.CheckboxSelectMultiple(
        attrs = {
            'data-toggle': 'tooltip',
            'data-placement': 'right',
            'title': 'Check/uncheck to show specific user group'
            }
        ),
        queryset=queryset_,\
        empty_label=None
    )
    active = forms.BooleanField(initial=True, widget=forms.CheckboxInput(
            attrs = {
                'data-toggle': 'tooltip',
                'data-placement': 'right',
                'title': 'Apply filter for active or inactive users'
                }
    ))
    all_users = forms.BooleanField(initial=False, widget=forms.CheckboxInput(
            attrs = {
                'data-toggle': 'tooltip',
                'data-placement': 'right',
                'title': 'Toggle to show all users'
                }
    ))

class ElectionFilterForm(forms.Form):
    school_year = forms.ModelChoiceField(
                queryset=Election
                .all_objects.all().order_by('school_year')\
                .values_list('school_year',flat=True).distinct(),
                widget=forms.Select(
                attrs = {
                    'data-toggle': 'tooltip',
                    'data-placement': 'right',
                    'title': 'Apply filter by school year'
                    }
                    )
                )

class ElectionForm(forms.ModelForm):
    #get all distinct school year from class model
    #create a list and convert to tuple
    SCHOOL_YEAR_CHOICES = tuple(
                [ (school_year,school_year) for school_year in Class.objects.all()\
                .order_by('-school_year')\
                .values_list('school_year',flat=True).distinct('school_year')
                ]
            )
    school_year = forms.ChoiceField(
                choices=SCHOOL_YEAR_CHOICES
    )
    field_order = [
                'school_year',
                'name',
                'description',
                'positions',
                'election_day_from',
                'election_day_to',
    ]

    class Meta:
        model = Election
        fields = (
                'school_year',
                'name',
                'description',
                'positions',
                'election_day_from',
                'election_day_to',
        )
        widgets = {
            'election_day_from': forms.DateInput(format = '%m/%d/%Y',attrs={'class':'datepicker'}, ),
            'election_day_to': forms.DateInput(format = '%m/%d/%Y',attrs={'class':'datepicker'}),
            'description': forms.Textarea(),
        }

    def clean_election_day_to(self):
        cleaned_data = super().clean()
        election_day_from = cleaned_data.get('election_day_from',None)
        election_day_to = cleaned_data['election_day_to']

        #check if from is blank, raise error
        if not election_day_from:
            raise forms.ValidationError(
                "Start Date should not be empty."
            )

        #from day should be less than
        if election_day_from > election_day_to:
                raise forms.ValidationError(
                    "Date range invalid. Start date should not be greater than End date. "
                )
        #check for day overlap on existing object on the database
        if self.instance.pk == None: #for insert
            election_list = Election.objects.filter(
                            Q(election_day_from__gte=election_day_from,
                                election_day_to__lte=election_day_from)
                            | Q(election_day_from__gte=election_day_to,
                                election_day_to__lte=election_day_to)
                            | Q(election_day_from__gte=election_day_from,
                                election_day_from__lte=election_day_to)
                            | Q(election_day_to__gte=election_day_from,
                                election_day_to__lte=election_day_to)
                            )
        else: #for update
            election_list = Election.objects.filter(
                            Q(election_day_from__gte=election_day_from,
                                election_day_to__lte=election_day_from)
                            | Q(election_day_from__gte=election_day_to,
                                election_day_to__lte=election_day_to)
                            | Q(election_day_from__gte=election_day_from,
                                election_day_from__lte=election_day_to)
                            | Q(election_day_to__gte=election_day_from,
                                election_day_to__lte=election_day_to),
                                ~Q(id = self.instance.pk) #exclude instance to be updated
                            )
        if election_list:
            raise forms.ValidationError(
                "An existing election exist that overlap the date specified."
            )
        return election_day_to

    def clean_school_year(self):
        cleaned_data = super().clean()
        school_year = cleaned_data['school_year']
        if not school_year:
            raise forms.ValidationError(
                "Invalid School Year. "
            )
        return school_year

class ElectionFormMoreDetails(ElectionForm):
    created_by = forms.CharField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
    last_updated_by = forms.CharField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['created_by'].initial = self.instance.created_by
        self.fields['last_updated_by'].initial = self.instance.last_updated_by
        for key in self.fields.items(): #set all field as readonly
            self.fields[key[0]].widget.attrs['disabled'] = True
        self.fields['positions'].widget.attrs['disabled'] = True
        self.fields['school_year'].widget.attrs['disabled'] = True

class PositionForm(forms.ModelForm):
    #get all distinct grade_level from class model
    #create a list and convert to tuple
    GRADE_LEVEL_CHOICES = tuple(
                [ (grade_level,grade_level) for grade_level in Class.objects.all()\
                .order_by('grade_level')\
                .values_list('grade_level',flat=True).distinct('grade_level')
                ]
    )
    grade_level = forms.MultipleChoiceField(
                widget=forms.SelectMultiple,
                choices=GRADE_LEVEL_CHOICES,
                initial=[choice[0] for choice in GRADE_LEVEL_CHOICES] #select all
    )
    field_order = [
                'title',
                'number_of_slots',
                'description',
                'grade_level'
    ]
    number_of_slots = forms.CharField(initial=1, help_text='A valid number, please.')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk: #for update
            # https://stackoverflow.com/questions/34270099/django-modelform-overriding-init
            self.fields['grade_level'].initial = [
                            grade_level for grade_level in self.instance.grade_levels.all()
                            ]
        else:
            self.fields['number_of_slots'].initial = 1

    def clean_number_of_slots(self):
        cleaned_data = super().clean()
        number_of_slots = cleaned_data['number_of_slots']
        if int(number_of_slots) < 1:
            raise forms.ValidationError(
            "Number of slots should not be less than 1."
            )
        return number_of_slots

    def clean_title(self):
        cleaned_data = super().clean()
        title = cleaned_data['title']
        if self.instance.pk == None: #for insert
            if Position.objects.filter(title__iexact=title).exists():
                raise forms.ValidationError(
                "Title " + title + " already exist."
                )
        return title

    class Meta:
        model = Position
        fields = (
                'title',
                'number_of_slots',
                'description',
        )
        widgets = {
            'description': forms.Textarea,
        }

class PositionFormMoreDetails(PositionForm):

    created_by = forms.CharField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
    last_updated_by = forms.CharField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['created_by'].initial = self.instance.created_by
            self.fields['last_updated_by'].initial = self.instance.last_updated_by
            for key in self.fields.items(): #set all field as readonly
                self.fields[key[0]].widget.attrs['disabled'] = True

            self.fields['grade_level'].widget.attrs['disabled'] = True

class GenericFilterForm(forms.Form):
    show_all = forms.BooleanField(initial=False, widget=forms.CheckboxInput(
            attrs = {
                'data-toggle': 'tooltip',
                'data-placement': 'right',
                'title': 'Toggle to show or hide inactive'
                }
    ))

class PartyForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = (
                'name',
        )

    def clean_name(self):
        cleaned_data = super().clean()
        name = cleaned_data['name']
        if self.instance.pk == None: #for insert
            if Party.objects.filter(name__iexact=name).exists():
                raise forms.ValidationError(
                "Party " + name + " already exist."
                )
        return name

class PartyFormMoreDetails(PartyForm):
    created_by = forms.CharField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
    last_updated_by = forms.CharField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['created_by'].initial = self.instance.created_by
            self.fields['last_updated_by'].initial = self.instance.last_updated_by
            for key in self.fields.items(): #set all field as disabled
                self.fields[key[0]].widget.attrs['disabled'] = True

class CandidateForm(forms.ModelForm):
    student =  forms.ChoiceField(widget = forms.Select(
                attrs = {
                    # 'data-toggle': 'tooltip',
                    # 'data-placement': 'right',
                    # 'title': 'Select the candidate from the list of students. Options will show after selecting Election.'
                    }
    ))
    position =  forms.ChoiceField(widget = forms.Select(
                attrs = {
                    # 'data-toggle': 'tooltip',
                    # 'data-placement': 'right',
                    # 'title': 'Select position. Options will show after selecting Election.'
                    }
    ))

    class Meta:
        model = Candidate
        fields = (
                'election',
                'position',
                'student',
                'party',
        )
