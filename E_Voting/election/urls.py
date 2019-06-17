from django.urls import path
from election.viewsF import vote,live_monitoring

app_name = 'election'

urlpatterns = [
    path('ajax/voter/authenticate/', vote.authenticate_voter_ajax,
        name='authenticate_voter_ajax'
    ),
    path('ajax/voter/confirmation/<int:pk>',
        vote.show_voter_confirmation_ajax,
        name='confirm_voter_ajax'
    ),
    path('ajax/voter/ballot/<int:voter_id>',
        vote.show_voter_ballot_ajax,
        name='voter_ballot_ajax'
    ),
    path('liveVoteMonitoring/',
        live_monitoring.ElectionLiveMonitoring.as_view(),
        name='election_live_monitoring'
    ),
    path('ajax/populate_vote_count/',
        live_monitoring.populate_vote_count_ajax,
        name='populate_vote_count_live'
    ),
    path('ajax/check_for_new_vote/',
        live_monitoring.check_for_new_vote_ajax,
        name='check_for_new_vote_ajax'
    ),
    path('ajax/review_voters_vote_auth/',
        vote.review_voters_vote_auth_ajax,
        name='review_voters_vote_auth_ajax'
    ),
    path('ajax/populate_participation_rate_live/',
        live_monitoring.populate_participation_rate_ajax,
        name='election_live_populate_participation_rate'
    ),
    ]
