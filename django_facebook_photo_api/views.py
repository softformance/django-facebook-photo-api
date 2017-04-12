import logging
import requests

from .models import FacebookApp, Hashtag, Post
from .utils import sync_by_tag, api_facebook
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

logger = logging.getLogger('default')

@login_required()
def sync_by_app(request, app_id=None):

    if not app_id:
        app_id = request.POST['app_id']
    if not app_id:
        return

    app = FacebookApp.objects.get(id=app_id)
    api = api_facebook(app_id)

    is_show = FacebookApp.objects.get(id=app_id).hashtag_is_show
    tags = Hashtag.objects.filter(application_id=app_id)
    for tag in tags:
        sync_by_tag(app_id, tag, is_show, api)

    return redirect(reverse('admin:%s_%s_changelist' % (
        app._meta.app_label, 'post')))


def get_posts(request, app_id):
    order_by_param = ('?', 'created_at')
    try:
        app = FacebookApp.objects.get(id=app_id)
    except:
        return []

    #count
    try:
        count = int(request.GET.get('count'))
    except:
        count = app.hashtag_count

    #order_by
    if request.GET.get('order_by') in order_by_param:
        order_by = request.GET.get('order_by')
    else:
        order_by = app.hashtag_sort_by

    params = {'application_id': app_id}
    tags = request.GET.getlist('tags')
    if tags:
        params['hashtags__name__in'] = tags

    posts = Post.objects.filter(**params)\
        .filter(show=True) \
        .order_by(order_by) \
        .values('media_id', 'photo', 'link', 'caption', 'photo_height', 
            'photo_width')[:count]

    result_dict = {}
    result_dict['from_site'] = 'facebook'
    result_dict['photos'] = list(posts)

    return JsonResponse(result_dict)
