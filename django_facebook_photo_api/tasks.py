from __future__ import absolute_import, unicode_literals
from celery import shared_task

import tweepy
from django_facebook_photo_api.models import FacebookApp, Hashtag, Post, Subscription
from django_facebook_photo_api.utils import sync_by_tag, save_post, api_facebook


@shared_task(name='Sync Facebook application by id')
def sync_hashtag_by_app_id(*args):
    for app_id in args:
        try:
            app = FacebookApp.objects.get(pk=app_id)
        except FacebookApp.DoesNotExist:
            print('DOESNOT EXIST')
            continue

        is_show = app.hashtag_is_show
        api = api_facebook(int(app_id))

        tags = Hashtag.objects.filter(application_id=app_id)
        for tag in tags:
            sync_by_tag(app_id, tag, is_show, api)