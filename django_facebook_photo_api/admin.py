import os
import requests

from django import forms
from datetime import datetime
from django.urls import reverse
from django.contrib import admin
from django.conf.urls import url
from django.core.files.base import ContentFile
from django.forms.models import ModelForm

from .utils import get_media_by_url
from .models import Post, Hashtag, FacebookApp, Subscription


class PostUrlForm(forms.ModelForm):
    url = forms.URLField(label='Insert link to tweet', required=True,
            widget=forms.URLInput(attrs={'placeholder':
             'https://www.facebook.com/softformance/photos/a.696731120492869.1073741828.289257041240281/696730657159582/?type=3&theater'}))

    class Meta:
        model = Post
        fields = ['application', 'url']

    def clean(self):
        cleaned_data = super(PostUrlForm, self).clean()
        if not cleaned_data.get('application'):
            raise forms.ValidationError("Please, select application")
        elif not cleaned_data.get('url'):
            raise forms.ValidationError("Please, insert URL")
        error, data = get_media_by_url(
            cleaned_data['application'], cleaned_data['url'])

        if error:
            raise forms.ValidationError(error)
        if data:
            cleaned_data['data'] = data
        else:
            raise forms.ValidationError("Please, insert link with photo")

        return cleaned_data


class PostAdmin(admin.ModelAdmin):

    change_list_template = 'admin/post_change_list.html'

    list_display = ('application', 'thumb_image', 'get_username', 'caption',
                    'get_hashtags', 'created_at', 'show',)
    list_display_links = ('caption', )
    list_filter = ('application', 'hashtags', 'created_at', )
    list_editable = ('show', )
    search_fields = ['caption', 'tags__name']

    def save_model(self, request, obj, form, change):
        if request.POST.get('url'):
            data = form.cleaned_data
            data_facebook = data['data']
            obj.media_id = data_facebook['id']
            obj.link = data_facebook['link']
            obj.caption = data_facebook['name']
            media_url = data_facebook['images'][0]['source']
            obj.created_at = data_facebook['created_time']
            obj.username = data_facebook['from']['id']
            # save image
            photo_content = ContentFile(requests.get(media_url).content)
            obj.photo.save(os.path.basename(media_url), photo_content)
            # save tags
            app_hashtags = Hashtag.objects.filter(application_id=data['application'].id).iterator()
            hashtags_from_url_page = [word[1:].lower() for word in data_facebook['name'].split() if word.startswith('#')]
            hashtags_list = [tag for tag in app_hashtags for hashtag in hashtags_from_url_page if tag.name == hashtag]
            for hashtag in hashtags_list:
                obj.hashtags.add(hashtag)
            if hashtags_list:
                obj.save()
            return

        obj.save()

    def get_apps(self):
        return FacebookApp.objects.all()

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['apps'] = self.get_apps()
        return super(PostAdmin, self).changelist_view(
            request, extra_context=extra_context)

    def get_hashtags(self, obj):
        return ", ".join([tag.name for tag in obj.hashtags.all()])

    def thumb_image(self, obj):
        return '<a href="%s" target="_blank"><img src="%s"/></a>' % (
            obj.link, obj.get_thumb_url())

    def get_username(self, obj):
        if obj.username:
            return '<a href="https://www.facebook.com/%s" target="_blank">@%s</a>' % (
                obj.username, obj.username)

    def get_urls(self):
        urls = super(PostAdmin, self).get_urls()
        c_urls = [
            url(r'^add_by_url/$', self.add_by_url),
        ]
        return c_urls + urls

    def add_by_url(self, request):
        return self.add_view(request, form=PostUrlForm)

    def add_view(self, request, form=ModelForm, form_url='',
                 extra_context=None):
        self.form = form
        return super(PostAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.form = ModelForm
        return super(PostAdmin, self).change_view(request, object_id, form_url,
                                                  extra_context)

    thumb_image.allow_tags = True
    get_username.allow_tags = True


class HashtagAdmin(admin.ModelAdmin):

    list_display = ('name',)
    list_filter = ('name', )


class FacebookAppAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')
    fieldsets = (
        (None, {
            'fields': ('name', 'access_token'),
            'classes': ('extrapretty', 'wide'),
        }),
        ('Hashtag options', {
            'fields': ('hashtag_is_show', 'hashtag_sort_by', 'hashtag_count'),
            'classes': ('extrapretty', 'wide', ),
        }),
    )

    def response_change(self, request, obj):
        response = super(FacebookAppAdmin, self).response_change(request, obj)

        return response

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('url', 'facebook_id', 'get_hashtags', 'type')

    def get_hashtags(self, obj):
        return list(obj.hashtags.all())
    get_hashtags.short_description = "Hashtags"


admin.site.register(FacebookApp, FacebookAppAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(Subscription, SubscriptionAdmin)

