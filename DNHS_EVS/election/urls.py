from django.urls import path
from election.viewsF import vote

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
        name='show_voter_ballot_ajax'
    ),
    ]
