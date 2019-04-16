from reporting.management.helpers.bulk_create_helper import BulkCreateManager
from reporting.models import DenormalizedVotes
from  registration.models import VoteArchived,Vote
from registration.management.helpers.db_object_helpers import truncate_table

def delete_election_in_DenormalizedVotes(election):
    DenormalizedVotes.objects.filter(election_id=election.id).delete()

def delete_election_in_VoteArchived(election):
    VoteArchived.objects.filter(election_id=election.id).delete()

def denormalized_election(election):
    '''
        Call this from view, can't be call in model. Got circular reference error.
        Make sure election status is FINALIZED before calling this method
        Denormalized all votes for analysis.
        Denormalized table is optimized for select queries which is heavily
            used in reporting
        Steps:
            1. Delete all records in DenormalizedVotes table for this election
                No Delete for security purposes. This action should be done only once per election.
            2. populate DenormalizedVotes table and VoteArchive Table
            3. validate
                count the source and compare the count in the target
                if matched then return True if Not return False and delete all inserted
                    records in DenormalizedVotes and VoteArchive
            4. Update the given election to status COMPLETED

    '''
    if election.status != 'FINALIZED':
        return False

    # # step 1. Delete all record in DenormalizedVotes model for the given election
    # # this is to avoid duplicates
    # delete_election_in_DenormalizedVotes(election)

    # step 2. populate DenormalizedVotes and VoteArchive
    # get all voters of the election
    voters = election.voters.all()
    bulk_mgr = BulkCreateManager(chunk_size=200) #commit every 200 records
    bulk_mgr_vote_archive = BulkCreateManager(chunk_size=200)

    vote_counter = 0
    for voter in voters:
        # in every voter, get the votes by accessing the voter's ballot
        if voter.ballot != None: #make sure voter has voted
            for vote in voter.ballot.votes.all():
                # print(vote.candidate.id)
                bulk_mgr.add(DenormalizedVotes(
                    voter_id_h = voter.hash_id,
                    voter_sex = voter.student.sex.sex,
                    voter_age = voter.student.age,
                    voter_mother_tongue = voter.student.mother_tongue.mother_tongue,
                    voter_ethnic_group = voter.student.ethnic_group.ethnic_group,
                    voter_religion = voter.student.religion.religion,
                    voter_address_barangay = voter.student.address_barangay.address_barangay,
                    voter_address_municipality = voter.student.address_municipality.address_municipality,
                    voter_address_province = voter.student.address_province.address_province,
                    voter_class_grade_level = voter.student_class.grade_level,
                    voter_class_section = voter.student_class.section,
                    candidate_name = vote.candidate.student.__str__(),
                    candidate_sex = vote.candidate.student.sex.sex,
                    candidate_age = vote.candidate.student.age,
                    candidate_mother_tongue = vote.candidate.student.mother_tongue.mother_tongue,
                    candidate_ethnic_group = vote.candidate.student.ethnic_group.ethnic_group,
                    candidate_religion = vote.candidate.student.religion.religion,
                    candidate_address_barangay = vote.candidate.student.address_barangay.address_barangay,
                    candidate_address_municipality = vote.candidate.student.address_municipality.address_municipality,
                    candidate_address_province = vote.candidate.student.address_province.address_province,
                    candidate_class_grade_level = vote.candidate.candidate_class.grade_level,
                    candidate_class_section = vote.candidate.candidate_class.section,
                    candidate_party = vote.candidate.party.name,
                    candidate_position = vote.candidate.position.title,
                    candidate_position_number_of_slots = vote.candidate.position.number_of_slots,
                    election_id = vote.candidate.election.id,
                    election_name = vote.candidate.election.name,
                    election_school_year = vote.candidate.election.school_year,
                    election_day_from = vote.candidate.election.election_day_from,
                    election_day_to = vote.candidate.election.election_day_to,
                    candidate_position_priority = vote.candidate.position.priority
                    )
                )
                bulk_mgr_vote_archive.add(VoteArchived(
                    hashed_id = vote.hashed_id,
                    ballot = vote.ballot,
                    candidate = vote.candidate,
                    election = vote.candidate.election
                    )
                )
                vote_counter += 1 #increment counter every add. Use to matched the number inserted and source
            bulk_mgr.done()
            bulk_mgr_vote_archive.done()

    # step 3. validate the count
    DenormalizedVotes_count = DenormalizedVotes.objects.filter(
                                    election_id=election.id
                                ).count()
    if vote_counter != DenormalizedVotes_count:
        # rollback. delete all inserted record for the given election
        delete_election_in_DenormalizedVotes(election)
        return False
    else:
        truncate_table(Vote)
        election.status = 'COMPLETED'
        election.save()
        return True
