from django import forms
from registration.models import Election



def get_election_choices():
    ELECTION_CHOICES = tuple(
        [ (election.id, election.__str__()) for election in Election.objects.filter(
                            status='COMPLETED'
                            )
        ]
        # [ (election.id, election.__str__()) for election in Election.objects.all()
        # ]
    )
    return ELECTION_CHOICES

class ElectionFilterForm(forms.Form):

    DISTRIBUTION_CHOICES = (
            ('voter_class_section', 'By Section'),
            ('voter_class_grade_level', 'By Grade Level'),
            ('voter_sex', 'By Gender'),
            ('voter_age', 'By Age'),
            ('voter_address_barangay', 'By Barangay Adress'),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['election'] = forms.ChoiceField(
                    choices=get_election_choices(),
                    widget=forms.Select(
                        attrs = {
                            'data-toggle': 'tooltip',
                            'data-placement': 'left',
                            'title': 'Change Election'
                            }
                    ),
                    required=False,
        )
        self.fields['distribution'] = forms.ChoiceField(
                    choices=self.DISTRIBUTION_CHOICES,
                    required=False,
                    )

class ElectionResultFilterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['election'] = forms.ChoiceField(
                    choices=get_election_choices(),
                    widget=forms.Select(
                        attrs = {
                            'data-toggle': 'tooltip',
                            'data-placement': 'left',
                            'title': 'Change Election'
                            }
                    ),
                    required=False,
        )
