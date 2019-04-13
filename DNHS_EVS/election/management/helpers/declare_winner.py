from registration.models import Vote,WinnerCandidate
from operator import itemgetter
from reporting.management.helpers.bulk_create_helper import BulkCreateManager

def declare_winners(election):
    '''
        For a given election, declare the winners based on the votes
        Detect if there is a tie, System admin will manually delete the winner
            after the 'toss-coin'
        Steps:
            Algo #1
            1. Get positions of the election
            2. Iterate positions
            3. Iterate candidate for every position and get the votes
            4. Create list of dictionaries for candidate and vote_count
            5. sort the list by vote_count using reverse=True
                https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary
            6. get the winners depending on number of slots
            7. Check for a tie
    '''

    winner_candidate_bulk_mgr = BulkCreateManager(chunk_size=100)

    # 1
    positions = election.positions.all()

    # 2
    for position in positions:
        # 3
        candidate_list = list()
        for candidate in position.candidates.filter(election=election):
            candidate_dictionary = dict()
            candidate_dictionary['candidate'] = candidate
            candidate_dictionary['vote_count'] = candidate.votes.count()
            candidate_dictionary['tie_flag'] = False
            # 4
            candidate_list.append(candidate_dictionary)

        # 5
        candidate_list = sorted(
                            candidate_list,
                            key=itemgetter('vote_count'),
                            reverse=True
                        )

        # 6
        number_of_slots = position.number_of_slots
        winner_list = candidate_list[:number_of_slots]
        tie_flag = False

        # 7
        tie_pointer = number_of_slots  #to prevent out of range error

        while len(candidate_list) > tie_pointer \
            and candidate_list[tie_pointer]['vote_count'] == winner_list[-1]['vote_count']:
            winner_list.append(candidate_list[tie_pointer])
            tie_pointer += 1
            tie_flag = True

        if tie_flag:
            # check from the end of winner_list
            # get the vote_count
            tie_vote_count = winner_list[-1]['vote_count']

            #check all in the winner_list which have the same number of tie_vote_count
                #then flagged as tie True
            for winner in winner_list:
                if winner['vote_count'] == tie_vote_count:
                    winner['tie_flag'] = True

        #8 Push to the database using bulk_manager
        for winner in winner_list:
            winner_candidate_bulk_mgr.add(WinnerCandidate(
                        election = election,
                        candidate = winner['candidate'],
                        tie = winner['tie_flag']
                    )
            )
    winner_candidate_bulk_mgr.done()
