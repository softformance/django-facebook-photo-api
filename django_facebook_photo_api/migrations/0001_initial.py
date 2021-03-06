# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-17 17:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import easy_thumbnails.fields
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Application Name')),
                ('access_token', models.CharField(max_length=100, verbose_name='Access token')),
                ('hashtag_is_show', models.BooleanField(default=False, verbose_name='Show posts')),
                ('hashtag_sort_by', models.CharField(choices=[('created_at', 'DATE'), ('?', 'RANDOM')], default='date', max_length=60, verbose_name='Type of sort')),
                ('hashtag_count', models.PositiveSmallIntegerField(default=6)),
            ],
            options={
                'verbose_name': 'Facebook Application',
                'verbose_name_plural': 'Facebook Applications',
            },
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Hashtag name')),
                ('application', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='app_hashtag', to='django_facebook_photo_api.FacebookApp')),
            ],
            options={
                'verbose_name': 'Hashtag',
                'verbose_name_plural': 'Hashtags',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_id', models.CharField(max_length=100, verbose_name='Media ID')),
                ('photo', easy_thumbnails.fields.ThumbnailerImageField(height_field='photo_height', upload_to='facebook_photos', width_field='photo_width')),
                ('photo_height', models.PositiveIntegerField(default=0, editable=False)),
                ('photo_width', models.PositiveIntegerField(default=0, editable=False)),
                ('link', models.URLField(verbose_name='Link')),
                ('caption', models.TextField(blank=True, default='', null=True, verbose_name='Caption text')),
                ('username', models.CharField(blank=True, max_length=100, null=True, verbose_name='Facebook username')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('show', models.BooleanField(default=False)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='app_post', to='django_facebook_photo_api.FacebookApp')),
                ('hashtags', models.ManyToManyField(to='django_facebook_photo_api.Hashtag')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(help_text='Please insert here clear link to Page or Group ')),
                ('facebook_id', models.BigIntegerField(default=0, editable=False)),
                ('last_synced_post', jsonfield.fields.JSONField(blank=True, default={}, editable=False)),
                ('type', models.CharField(blank=True, choices=[('group', 'Group'), ('page', 'Page')], editable=False, max_length=60, verbose_name='Type of subscription')),
                ('application', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='app_subscription', to='django_facebook_photo_api.FacebookApp')),
            ],
        ),
        migrations.CreateModel(
            name='TaskShedulerFacebook',
            fields=[
                ('periodictask_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_celery_beat.PeriodicTask')),
                ('periodic_task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='periodic_task', to='django_facebook_photo_api.FacebookApp')),
            ],
            bases=('django_celery_beat.periodictask',),
        ),
        migrations.AlterUniqueTogether(
            name='subscription',
            unique_together=set([('application', 'url')]),
        ),
        migrations.AlterUniqueTogether(
            name='post',
            unique_together=set([('application', 'media_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='hashtag',
            unique_together=set([('application', 'name')]),
        ),
    ]
