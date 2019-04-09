from django.db import models
from registration import models as RegistrationModels
from django.conf import settings
from election.management.helpers.hasher_helpers import MyHasher
import uuid

# Create your models here.
class Ballot(RegistrationModels.BaseModel):
    vote_casted_timestamp = models.DateTimeField(null=False)
    vote_casting_IP = models.GenericIPAddressField(null=True)
    # https://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
    # request.META.get('REMOTE_ADDR')
    voter_id_h = models.CharField(
            max_length=255,
            verbose_name="Hashed Voter ID",
            null=False,
            default=uuid.uuid4().hex,
            unique=True
    )

    def assign_voter_id(self, voter):
        self.voter_id_h = voter.hash_id
