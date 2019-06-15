
def arcive_vote(election):
    '''
        Archives the vote of the given election.
        Move the data from Vote to VoteArchive.
        This is to optimized voting experience by not bloating-out Vote Table
        This function is moved to denormalizer so it will minimize db hit
        Steps:
            1. Copy all votes of the given election from Vote to VoteArchive
            2. Check if number of votes matched

    '''
    pass
