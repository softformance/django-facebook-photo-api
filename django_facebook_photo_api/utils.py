import os
import logging
import requests
import facebook
import urllib.parse as urlparse

from django.core.files.base import ContentFile
from .models import Post, Hashtag, FacebookApp
from .app_settings import FACEBOOK_API_VERSION

logger = logging.getLogger('default')


def get_media_by_code(facebook_id, id_application):
    try:
        api = api_facebook(id_application)
        media_object = api.get_object(id=str(facebook_id), 
            fields="id,name,created_time,from,link,images")
        return None, media_object
    except:
        error = "Error while fetching."
        logger.exception(error)
        return error, None


def save_post(app_id, feed_post, is_show, hashtag):
    media_id = feed_post['object_id']
    link = feed_post['permalink_url']
    caption = feed_post['message']
    media_url = feed_post['full_picture']
    created_at = feed_post['created_time']
    username = feed_post['from']['id']

    post, created = Post.objects.get_or_create(
        media_id=media_id, application_id=app_id,
        defaults={
            'link': link,
            'username': username,
            'caption': caption,
            'created_at': created_at,
            'show': is_show
        }
    )

    if created:
        # save image
        photo_content = ContentFile(requests.get(media_url).content)
        post.photo.save(os.path.basename(media_url), photo_content)
        # save tags
        app_hashtags = Hashtag.objects.filter(application_id=app_id).iterator()
        hashtags_from_url_page = [word[1:].lower() for word in feed_post['message'].split() if word.startswith('#')]
        hashtags_list = [tag for tag in app_hashtags for hashtag in hashtags_from_url_page if tag.name == hashtag]
        for hashtag in hashtags_list:
            post.hashtags.add(hashtag)
        if hashtags_list:
            post.save()
    return post


def get_media_by_url(application, url):
    parsed = urlparse.urlparse(url)
    if urlparse.urlparse(url).path == '/photo.php':
        # Verify if it photo from group 
        facebook_id = urlparse.parse_qs(parsed.query)['fbid'][0]
    elif list(filter(None, parsed.path.split('/')))[1] == 'photos':
        # Verify if it photo from page
        facebook_id = list(filter(None, parsed.path.split('/')))[-1]
    return get_media_by_code(facebook_id, application.id)


def sync_by_tag(app_id, tag, is_show, api):
    #TODO pagination
    hashtag = '#' + str(tag.name)
    api = api_facebook(app_id)
    for subscription in tag.subscriptions.all():
        feeds = api.get_connections(id=subscription.facebook_id, connection_name='feed',
            fields="object_id,id,message,created_time, \
            permalink_url,type,from,full_picture")
        for feed_post in feeds['data']:
            if feed_post['type'] == 'photo' and feed_post.get('message') != None and hashtag in feed_post.get('message'):
                save_post(app_id, feed_post, is_show, tag)

def api_facebook(app_id):
    try:
        app = FacebookApp.objects.get(id=app_id)
        is_show = app.hashtag_is_show
        oauth_data = {}
        oauth_data['access_token'] = app.access_token
    except:
        message = "Cannot get application."
        logger.exception(message)
        return None

    try:
        api = facebook.GraphAPI(access_token=oauth_data['access_token'], version=FACEBOOK_API_VERSION)
        return api
    except:
        message = "Error. Verify your access token."
        logger.exception(message)
        return None