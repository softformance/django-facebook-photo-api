=============================
Django Facebook photo api
=============================

.. image:: https://badge.fury.io/py/Django-Facebook-photo-api.svg
    :target: https://badge.fury.io/py/Django-Facebook-photo-api

.. image:: https://travis-ci.org/SoftFormance/Django-Facebook-photo-api.svg?branch=master
    :target: https://travis-ci.org/SoftFormance/Django-Facebook-photo-api

.. image:: https://codecov.io/gh/SoftFormance/Django-Facebook-photo-api/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/SoftFormance/Django-Facebook-photo-api

Get photos from Facebook page or group by hashtags. 

Documentation
-------------

The full documentation is at https://django-facebook-photo-api.readthedocs.io.

Quickstart
----------

Install Django Facebook photo api from PyPi::

    pip install django-facebook-photo-api

Install Django Facebook photo api from GitHub and install all dependencies::

    virtualenv photostream
    source photostream/bin/activate
    pip install -e git+https://github.com/softformance/django-facebook-photo-api.git#egg=django-facebook-photo-api
    pip install -e git+https://github.com/mobolic/facebook-sdk.git#egg=facebook-sdk

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_facebook_photo_api',
        ...
    )

Add Django Facebook photo api's URL patterns:

.. code-block:: python

    from django_facebook_photo_api import urls as django_facebook_photo_api_urls


    urlpatterns = [
        ...
        url(r'^facebook_app/', include(django_facebook_photo_api_urls, 
            namespace="facebook-feed")),
        ...
    ]

- Create at `Facebook for developers <https://developers.facebook.com/>`_ new application.
- Open `Graph API Explorer <https://developers.facebook.com/tools/explorer/>`_ and choose your new generated application in the upper right corner.
- Add into Django admin ``Facebook application`` model your access token from *Access Token* field in Graph API Explorer.
- Add pages or groups into ``Subscriptions`` model which you want to follow up.
- Add hashtag to your ``Hashtags`` model and assign hashtags to subscriptions


Features
--------

* Retrieve from Facebook photos by hashtag in selected pages or groups. 
* Synchronization of retrieving photos from Facebook page or group.
* Sync subscriptions, add a post by URL and add post manually.
* Get photos from your backend server by simple URL.

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
