# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from django_facebook_photo_api.urls import urlpatterns as django_facebook_photo_api_urls

urlpatterns = [
    url(r'^', include(django_facebook_photo_api_urls, namespace='django_facebook_photo_api')),
]
