from election import forms
from django.template.loader import render_to_string
from django.http import JsonResponse
from registration.models import Election,Voter,Candidate,Vote
from registration.models_election import Position
from django.core import serializers
from django.shortcuts import get_object_or_404
from election.models import Ballot
from datetime import datetime
from registration.management.helpers.token_generator import id_generator
from election.management.helpers.hasher_helpers import MyHasher
from django.conf import settings
from operator import itemgetter

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
        form = forms.OfficialBallotForm(request.POST, voter=voter)
        if form.is_valid():
            #get client's IP
            ip = None
            if request.META.get('HTTP_X_FORWARDED_FOR'):
                ip = request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            #create ballot for this voter
            ballot = Ballot(
                    vote_casted_timestamp = datetime.now(),
                    vote_casting_IP = ip
            )
            ballot.assign_voter_id(voter)
            ballot.save()
            # get the canidates that the voter voted
            for position,candidates in form.cleaned_data.items():
                for candidate in candidates:
                    #push the vote on the database
                    vote = Vote(
                        ballot=ballot,
                        candidate=Candidate.objects.get(id=int(candidate))
                    )
                    # to validate the vote. withouth this, this vote will be tagged
                    #  as invalid
                    vote.populate_hashed_id()
                    vote.save()

            #update the voter's recored to tagged as voted
            voter.is_vote_casted = True

            voter_validation_token = voter.assign_voter_token_for_validation_h()
            voter.save()

            data['form_is_valid'] = True
            context['voter_validation_token'] = voter_validation_token
            data['html_form'] = render_to_string(
                    'election/partial_vote_casting_confirmation.html',
                    context,
                    request=request
            )
        else:
            data['form_is_valid'] = False
            context['object'] = voter
            context['form'] = form
            context['candidates'] = form.candidate_list
            data['html_form'] = render_to_string(
                    'election/partial_voter_ballot.html',
                    context,
                    request=request
            )

    else:
        #the magic is in the form
        form = forms.OfficialBallotForm(voter=voter)
        context['form'] = form
        context['candidates'] = form.candidate_list
        data['html_form'] = render_to_string(
                'election/partial_voter_ballot.html',
                context,
                request=request
        )
    return JsonResponse(data)

def review_voters_vote_auth_ajax(request):
    '''
        Handles the modal that will authenticate the voter by enetring his/her
            token and secret password
    '''
    data = dict()
    context= dict()
    if request.method == 'POST':
        form = forms.VoterReviewVoteAuthenticate(data=request.POST)
        if form.is_valid():
            votes = None
            if form.voter.election.status == 'COMPLETED':
                votes = form.voter.ballot.votes_archived.all().select_related('candidate')
            else:
                votes = form.voter.ballot.votes.all().select_related('candidate')
            # create list of dictinaries to sorted out by position priority
            votes_list = list()
            for vote in votes:
                vote_dict = dict()
                vote_dict['position'] = str(vote.candidate.position)
                vote_dict['candidate'] = str(vote.candidate.student)
                vote_dict['position_priority'] = vote.candidate.position.priority
                votes_list.append(vote_dict)
            # sort the votes_list by position.priority
            votes_list_sorted = sorted(votes_list, key=itemgetter('position_priority'))
            context['voter'] = form.voter.student.first_name
            context['votes'] = votes_list_sorted
            # print(votes_list_sorted)
            data['html_form_votes'] = render_to_string(
                    'election/partial_voters_review_vote.html',
                    context,
                    request = request
            )
            # print(data['html_form_votes'])
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
        # data['form_is_valid'] = False
    else:
        form = forms.VoterReviewVoteAuthenticate()

    context['form'] = form
    data['html_form'] = render_to_string(
            'election/partial_voters_review_vote_auth.html',
            context,
            request = request
    )
    return JsonResponse(data)
