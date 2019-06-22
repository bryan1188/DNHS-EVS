from E_Voting.settings.common import *

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '@r#ql!gfrgc5#6=9*7%*8(lha)!5os8kiqdqsex8#*85eoq&!!'
SECRET_KEY = os.environ['django_SECRET_KEY']

# hashing secret key
HASHING_SECRET_KEY =  os.environ['django_HASHING_SECRET_KEY']
HASHING_SALT =  os.environ['django_HASHING_SALT']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
