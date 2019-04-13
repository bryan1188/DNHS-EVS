from reporting.management.helpers.bulk_create_helper import BulkCreateManager
from reporting.models import DenomarmalizedVotes

def delete_election(election):
    DenomarmalizedVotes.objects.filter(election_id=election.id).delete()

def denomarlized_election(election):
    '''
        Denormalized all votes for analysis.
        Denormalized table is optimized for select queries which is heavily
            used in reporting
        Steps:
            1. Delete all records in DenomarmalizedVotes table for this election
            2. populate DenomarmalizedVotes table
            3. validate
                count the source and compare the count in the target
    '''
    # step 1. Delete all record in DenomarmalizedVotes model for the given election
    delete_election(election)

    # step 2. populate DenomarmalizedVotes
    # get all voters of the election
    voters = election.voters.all()
    bulk_mgr = BulkCreateManager(chunk_size=200) #commit every 200 records

    vote_counter = 0
    for voter in voters:
        # in every voter, get the votes by accessing the voter's ballot
        if voter.ballot != None: #make sure voter has voted
            for vote in voter.ballot.votes.all():
                # print(vote.candidate.id)
                bulk_mgr.add(DenomarmalizedVotes(
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
                    election_day_to = vote.candidate.election.election_day_to
                    )
                )
                vote_counter += 1 #increment counter every add
            bulk_mgr.done()

    # step 3. validate the count
    DenomarmalizedVotes_count = DenomarmalizedVotes.objects.filter(
                                    election_id=election.id
                                ).count()
    if vote_counter != DenomarmalizedVotes_count:
        # rollback. delete all inserted record for the given election
        delete_election(election)
        return False
    else:
        return True
