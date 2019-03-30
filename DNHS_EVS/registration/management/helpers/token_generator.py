import random
import string
import re

# https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
def id_generator(size = 6, chars = string.ascii_uppercase + string.digits):
    '''
        default size is 6 and default characters to randomized is all uppercase
            letters and numbers.
        Need to remove 0,O,I and 1 to avoid confusion
        Need to remove all white spaces
        remove symbols using regex
    '''
    chars = chars.upper() #convert to upper case
    chars = re.sub('[0O1I_ ]', '', chars) #remove 0, O, I, 1, _(underscore) and white spaces
    chars = re.sub(r'[^\w]', '', chars) #remove all symbols

    # https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

class BatchKeyGenerator():
    '''
        Class that generates a key in a batch.
        It includes a checking mechanism to make sure no duplicate key is
            generated.
    '''
    generated_key_set = set() #tracks all the generated key to check for duplicate
                            #use set instead of list for efficiency
    size = 6 #default size
    choice_chars = string.ascii_uppercase + string.digits #default char choices

    def __init__(self, *args, **kwargs):
        super().__init__()
        if 'size' in kwargs:
            self.size = kwargs.get('size')

    def generate_key(self, *args, **kwargs):
        '''
            generate random key based on the given chars.
            Check for duplicate from generated_key_set
        '''
        if 'size' in kwargs:
            size = kwargs.get('size')
        else:
            size = self.size

        if 'chars' in kwargs:
            chars = kwargs.get('chars')
        else:
            chars = self.choice_chars

        generated_key = id_generator(size, chars)
        while generated_key in self.generated_key_set: #make sure no duplicate
            generated_key = id_generator(size, chars)
            try_count += 1

        self.generated_key_set.add(generated_key)

        return generated_key
