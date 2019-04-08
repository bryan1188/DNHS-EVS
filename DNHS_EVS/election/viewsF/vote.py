from election import forms
from django.template.loader import render_to_string
from django.http import JsonResponse
from registration.models import Election,Voter,Candidate
from registration.models_election import Position
from django.core import serializers
from django.shortcuts import get_object_or_404

def authenticate_voter_ajax(request):
    '''
        handles the modal that will show on the home page during election day
        get the voter's token then authenticate
    '''
    data = dict()
    context = dict()
    context['object'] = Election.objects.get_current_election()

    if request.method == 'POST':
        form = forms.VoterAuthenticateForm(data=request.POST, election=context['object'])
        if form.is_valid():
            data['voter'] = serializers.serialize('json',[form.voter])
            data['token'] = form.cleaned_data['token']
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = forms.VoterAuthenticateForm()

    context['form'] = form
    data['html_form'] = render_to_string(
            'election/partial_voters_login_modal.html',
            context,
            request = request
    )
    return JsonResponse(data)

def show_voter_confirmation_ajax(request, pk):
    '''
        After token entered, show the voter's information for confirmation.
    '''
    data = dict()
    context = dict()
    voter = get_object_or_404(Voter, pk=pk)
    form = forms.VoterConfirmationForm(instance=voter)
    context['object'] = voter
    context['form'] = form
    data['html_form'] = render_to_string(
            'election/partial_voter_confirm.html',
            context,
            request=request
    )
    return JsonResponse(data)

def show_voter_ballot_ajax_to_remove(request, voter_id):
    '''
        after the voter confirmed, show the voter's ballot and start casting vote
        minimized database hits to improve performance. Pending action
    '''
    data = dict()
    context = dict()
    voter = get_object_or_404(Voter, pk=voter_id)
    context['candidates'] = Candidate.objects.get_candidate_of_voter(
                    voter.election,
                    voter.student_class.grade_level
                )
    positions = [
            candidate.position.__str__() for candidate in  context['candidates']
            ]
    context['positions'] = list(dict.fromkeys(positions)) #removes duplicate
    '''
        positions_with_candidate format:
            [
                { #position_dictionary format
                  "position": <position title, example President, Secretary>,
                  "candidates": [
                                    {
                                        "candidate_name": <from_student_name>,
                                        "candidate_id": <from Candidate object>,
                                        "counter": <for id tag in template>
                                    }
                                ],
                  "number_of_slots": <number_of_slots from Position>
                }
            ]
    '''
    positions_with_candidate = []
    position_dictionary = dict()
    for position in context['positions']:
        position_dictionary = {}
        position_dictionary['position'] = position
        position_candidate_list = []
        position_candidate_counter = 0
        for candidate in context['candidates'].filter(position__title=position):
            position_candidate = {}
            position_candidate['candidate_name'] = candidate.student.__str__()
            position_candidate['candidate_id'] = candidate.pk
            position_candidate['counter'] = position_candidate_counter
            position_candidate_list.append(position_candidate)
            position_candidate_counter += 1
        position_dictionary['candidates'] = position_candidate_list
        position_dictionary['number_of_slots'] = Position.objects.get(title=position).number_of_slots
        positions_with_candidate.append(position_dictionary)
    context['positions_with_candidate'] = positions_with_candidate
    form = forms.VoterConfirmationForm(instance=voter)
    context['object'] = voter
    context['form'] = form
    data['html_form'] = render_to_string(
            'election/partial_voter_ballot.html',
            context,
            request=request
    )
    return JsonResponse(data)

def show_voter_ballot_ajax(request, voter_id):
    '''
        acter the voter confirmed, show the voter's ballot and start casting vote
        minimized database hits to improve performance. Pending action
        use django forms instead of manually creating fields
    '''
    data = dict()
    context = dict()
    voter = get_object_or_404(Voter, pk=voter_id)
    context['object'] = voter
    if request.method == 'POST':
        print(request.POST)
        data['html_form'] = render_to_string(
                'election/partial_vote_casting_confirmation.html',
                context,
                request=request
        )
    else:
        #the magic is in the form
        form = forms.OfficialBallotForm(voter=voter)
        context['form'] = form
        data['html_form'] = render_to_string(
                'election/partial_voter_ballot.html',
                context,
                request=request
        )
    return JsonResponse(data)
