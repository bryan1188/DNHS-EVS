from django import forms
from registration.models import Voter,Candidate
from registration.models import Position
from django.contrib.auth.models import Group  #testing only, remove after testing

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
            # check if the voter voted already
            if voter_.is_vote_casted:
                raise forms.ValidationError(
                    "This token has been used already!"
                )
            else:
                self.voter = voter_
                return token

class VoterConfirmationForm(forms.ModelForm):
    voter_token = forms.CharField(required=False)
    voter_name = forms.CharField(required=False)
    voter_class = forms.CharField(required=False)

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

class OfficialBallotForm(forms.Form):
    '''
        official ballot of the voter.
        Dynamic number of fields based on the number of positions of the current election
    '''
    voter = None

    def __init__(self, *args, **kwargs):
        if kwargs.get('voter', None):
            self.voter = kwargs.get('voter')
            #after getting the data, delete passed argument to prevent error on calling super().__init__()
            del kwargs['voter']
        super().__init__(*args, **kwargs)
        # get first the candidates of this voter
        candidates = Candidate.objects.get_candidate_of_voter(
                        self.voter.election,
                        self.voter.student_class.grade_level
                    )
        # based on the list of candidates, get the positions available
        positions = [
                candidate.position.__str__() for candidate in  candidates
                ]
        for position in positions:
            field_name = position
            number_of_slots = Position.objects.get(title=position).number_of_slots
            # get the candidates for every position
            candidates_for_this_position = tuple([
                (candidate.pk, candidate.student.__str__()) \
                for candidate in candidates.filter(position__title=position)
                        ])
            self.fields[field_name] = forms.MultipleChoiceField(
                                widget=forms.CheckboxSelectMultiple(
                                        attrs = { #variable place holder that will be consumed on the template
                                            # this will determine how many allowed candidate per position
                                            'number-of-slots': number_of_slots,
                                             #this will identify the last element checked. Based on this number and number_of_slots,
                                             #other elements will be automatically unchecked
                                            'last-checked-counter': 0,
                                        },
                                    ),
                                choices=candidates_for_this_position,
                                required=False
                            )
            self.fields[field_name].label = "{}({})".format(field_name.title(),number_of_slots)

    def clean(self):
        cleaned_data = super().clean()
        for position,value in self.cleaned_data.items():
            if len(value) > Position.objects.get(title=position).number_of_slots:
                raise forms.ValidationError(
                    "Number of votes is more than the specified number of slots for {} position.".format(
                        position
                    )
                )

class VoterReviewVoteAuthenticate(forms.Form):
    token = forms.CharField()
    secret_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['token'].label = "Enter your TOKEN:"
        self.fields['secret_password'].label = "Enter your secret password:"
        self.voter = None

    def clean_token(self):
        cleaned_data = super().clean()
        token = cleaned_data['token'].upper()
        # use select related to cache the objects from election model
        # will be used later on the view
        self.voter = Voter.objects.select_related('election').filter(
                        voter_token=token
                        ).first()
        if not self.voter:
            raise forms.ValidationError(
                "This is not a valid token. Kindly check."
            )
        else:
            return token

    def clean_secret_password(self):
        cleaned_data = super().clean()
        secret_password = cleaned_data['secret_password']
        if self.voter:
            if not self.voter.authenticate_for_vote_validation(secret_password):
                raise forms.ValidationError(
                    "Invalid secret password."
                )
            else:
                return secret_password
        else:
            return secret_password
