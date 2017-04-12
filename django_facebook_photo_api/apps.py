# -*- coding: utf-8
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoFacebookPhotoApiConfig(AppConfig):
    name = 'django_facebook_photo_api'
    verbose_name = _("Facebook photostream backend")
