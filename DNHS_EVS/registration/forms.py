from django import forms
from registration.models import Student,UserProfile,Class
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
    student_lrn = forms.CharField(widget=forms.HiddenInput(), required=False)
    other_groups = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                      choices=FOR_OTHER_GROUPS_CHOICES, required=False)

    class Meta:
        model = User
        fields = ('username','password','confirm_password','last_name','first_name')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

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
