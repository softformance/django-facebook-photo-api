from django.conf import settings

#Insert here your settings const.
FACEBOOK_API_VERSION = getattr(settings, 'FACEBOOK_API_VERSION', '2.8')

FACEBOOK_APP_ID = getattr(settings, 'FACEBOOK_APP_ID', 1)

MEDIA_URL = getattr(settings, 'MEDIA_URL')