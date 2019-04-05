from django import forms
from registration.models import Voter

class VoterAuthenticateForm(forms.Form):
    token = forms.CharField()
    election = None
    # to minimized database hits, get the voter from this form and views will get it from here
    voter =  None

    def __init__(self, *args, **kwargs):
        if kwargs.get('election',None):
            self.election = kwargs.get('election')
            #after getting the data, delete passed argument to prevent error on calling super().__init__()
            del kwargs['election']
        super().__init__(*args, **kwargs)
        self.fields['token'].label = "Enter your TOKEN to cast your vote!"

    def clean_token(self):
        cleaned_data = super().clean()
        token = cleaned_data['token'].upper() # convert input to upper
        #check if token on Voter model exist based on the current election
        voter_ = Voter.objects.filter(voter_token=token, election=self.election).first()
        if not voter_:
            raise forms.ValidationError(
                "This is not a valid token for this election. Kindly check."
            )
        else:
            self.voter = voter_
            return token

class VoterConfirmationForm(forms.ModelForm):

    voter_name = forms.CharField()
    voter_class = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['voter_name'].initial = self.instance.student.name_title
            self.fields['voter_class'].initial = "{} - {}".format(
                                self.instance.student_class.grade_level,
                                self.instance.student_class.section
            )

        for key in self.fields.items(): #set all field as disabled
            self.fields[key[0]].widget.attrs['disabled'] = True
        self.fields['voter_name'].label = "Your Name"
        self.fields['voter_token'].label = "Your Token"
        self.fields['voter_class'].label = "Your Class"


    class Meta:
        model = Voter
        fields = ('voter_token',)
