# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _
from django.db.models import signals

from easy_thumbnails.fields import ThumbnailerImageField
from django_celery_beat.models import PeriodicTask, PeriodicTasks, \
    IntervalSchedule, CrontabSchedule, SolarSchedule
from jsonfield import JSONField


@python_2_unicode_compatible
class FacebookApp(models.Model):
    TYPE_OF_SORT = (
        ('created_at', 'DATE'),
        ('?', 'RANDOM'),
    )
    name = models.CharField(max_length=50, verbose_name=_('Application Name'))
    access_token = models.CharField(
        max_length=100, verbose_name=_('Access token'))
    hashtag_is_show = models.BooleanField(
        verbose_name=_('Show posts'), default=False)
    hashtag_sort_by = models.CharField(
        verbose_name=_('Type of sort'), choices=TYPE_OF_SORT, default='date', max_length=60)
    hashtag_count = models.PositiveSmallIntegerField(default=6)

    class Meta:
        verbose_name = _('Facebook Application')
        verbose_name_plural = _('Facebook Applications')

    def __str__(self):
        return '%s. %s' % (self.id, self.name)


@python_2_unicode_compatible
class TaskShedulerFacebook(PeriodicTask):
    periodic_task = models.ForeignKey(FacebookApp, on_delete=models.SET_NULL, 
        blank=True, null=True, related_name='periodic_task')


@python_2_unicode_compatible
class Hashtag(models.Model):
    application = models.ForeignKey(
        FacebookApp, related_name='app_hashtag', default=1)
    name = models.CharField(max_length=50, verbose_name=_('Hashtag name'))

    class Meta:
        verbose_name = _('Hashtag')
        verbose_name_plural = _('Hashtags')
        unique_together = (("application", "name"),) 

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower() 
        super(Hashtag, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Post(models.Model):
    application = models.ForeignKey(FacebookApp, related_name='app_post')
    media_id = models.CharField(_('Media ID'), max_length=100)
    photo = ThumbnailerImageField(upload_to='facebook_photos', height_field='photo_height', width_field='photo_width')
    photo_height = models.PositiveIntegerField(default=0, editable=False)
    photo_width = models.PositiveIntegerField(default=0, editable=False)
    link = models.URLField(_('Link'))
    hashtags = models.ManyToManyField(Hashtag)
    caption = models.TextField(
        verbose_name=_('Caption text'),
        default='', blank=True, null=True)
    username = models.CharField(
        _('Facebook username'), max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    show = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

        unique_together = (("application", "media_id"),)

    def get_thumb_url(self):
        try:
            return self.photo['thumb'].url
        except:
            return None


class Subscription(models.Model):
    TYPE_OF_SUBSCRIPTION = (
        ('group', 'Group'),
        ('page', 'Page'),
    )
    application = models.ForeignKey(
        FacebookApp, related_name='app_subscription', default=1)
    url = models.URLField(help_text="Please insert here clear link to Page or Group ")
    facebook_id = models.BigIntegerField(default=0, editable=False)
    last_synced_post = JSONField(default={}, blank=True, editable=False)
    type = models.CharField(
        verbose_name=_('Type of subscription'), choices=TYPE_OF_SUBSCRIPTION, max_length=60, 
        blank=True, editable=False)
    

    def save(self, *args, **kwargs):
        from .utils import api_facebook
        api = api_facebook(self.application.id)
        if '/groups/' in self.url:
            app_links_data = api.get_connections(id=str(self.url), 
                connection_name='app_links', fields='app_links')
            group_id = app_links_data['app_links']['android'][0]['url'].split('/')[-1]
            self.facebook_id = group_id
            self.type = 'group'
        else:
            self.facebook_id = api.get_object(id=str(self.url))['id']
            self.type = 'page'
        super(Subscription, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('application', 'url')

    def __str__(self):
        return self.url


signals.pre_delete.connect(PeriodicTasks.changed, sender=TaskShedulerFacebook)
signals.pre_save.connect(PeriodicTasks.changed, sender=TaskShedulerFacebook)
signals.pre_delete.connect(
    PeriodicTasks.update_changed, sender=IntervalSchedule)
signals.post_save.connect(
    PeriodicTasks.update_changed, sender=IntervalSchedule)
signals.post_delete.connect(
    PeriodicTasks.update_changed, sender=CrontabSchedule)
signals.post_save.connect(
    PeriodicTasks.update_changed, sender=CrontabSchedule)
signals.post_delete.connect(
    PeriodicTasks.update_changed, sender=SolarSchedule)
signals.post_save.connect(
    PeriodicTasks.update_changed, sender=SolarSchedule)