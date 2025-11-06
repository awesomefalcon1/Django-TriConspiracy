from django.conf import settings

class Constants:
    DEBUG = True
    SECRET_KEY = '1234567890'
    API_TOKEN = 'FOOBAR1'
    REDIS_URL = 'redis://localhost:6379'

settings.Constants = Constants
