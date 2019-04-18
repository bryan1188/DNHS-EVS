from django import forms
from registration.models import Election


ELECTION_CHOICES = tuple(
    # [ (election.id, election.__str__()) for election in Election.objects.filter(
    #                     status='COMPLETED'
    #                     )
    # ]
    [ (election.id, election.__str__()) for election in Election.objects.all()
    ]
)

class ElectionFilterForm(forms.Form):

    DISTRIBUTION_CHOICES = (
            ('voter_class_section', 'By Section'),
            ('voter_class_grade_level', 'By Grade Level'),
            ('voter_sex', 'By Gender'),
            ('voter_age', 'By Age'),
            ('voter_address_barangay', 'By Barangay Adress'),
    )
    election = forms.ChoiceField(
                choices=ELECTION_CHOICES,
                widget=forms.Select(
                    attrs = {
                        'data-toggle': 'tooltip',
                        'data-placement': 'left',
                        'title': 'Change Election'
                        }
                ),
    )
    distribution = forms.ChoiceField(
                choices=DISTRIBUTION_CHOICES
    )

class ElectionResultFilterForm(forms.Form):
    election = forms.ChoiceField(
                choices=ELECTION_CHOICES,
                widget=forms.Select(
                    attrs = {
                        'data-toggle': 'tooltip',
                        'data-placement': 'left',
                        'title': 'Change Election'
                        }
                ),
    )
