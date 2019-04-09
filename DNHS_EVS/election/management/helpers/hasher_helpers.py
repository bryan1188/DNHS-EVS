import uuid
import hashlib
from django.conf import settings

# https://www.pythoncentral.io/hashing-strings-with-python/
class MyHasher():
    hasher_lib = hashlib.sha1

    def hash(self, string_to_hash):
        salt = uuid.uuid4().hex
        # string_ = hashlib.sha512(string_to_hash.encode()).hexdigest + ':' + salt
        # return string_
        return self.hasher_lib(
                    salt.encode() + string_to_hash.encode()
                ).hexdigest() + str(':') + str(salt)

    def hash_fixed_salt(self, string_to_hash):
        salt = settings.HASHING_SALT
        # string_ = hashlib.sha512(string_to_hash.encode()).hexdigest + ':' + salt
        # return string_
        return self.hasher_lib(
                    salt.encode() + string_to_hash.encode()
                ).hexdigest()

    def check(self, hashed_string, string_to_check):
        string_, salt = hashed_string.split(':')
        return string_ == self.hasher_lib(
                            salt.encode() + string_to_check.encode()
                            ).hexdigest()
