from django import forms
from registration.models import Student,UserProfile,Class,ElectionOfficer
from django.contrib.auth.models import User,Group


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
    school_year = forms.ModelChoiceField( \
        queryset=Class.objects.all().order_by('school_year').values_list('school_year', flat=True).distinct())
    grade_level = forms.ChoiceField()
    section =  forms.ChoiceField()

class UserFilterForm(forms.Form):
    queryset_ =  Group.objects.all().order_by('name').values_list('name', flat=True).distinct()
    group = forms.ModelChoiceField(widget=forms.CheckboxSelectMultiple, \
        queryset=queryset_,\
        empty_label=None)
    active = forms.BooleanField(initial=True)
    all_users = forms.BooleanField(initial=False)
