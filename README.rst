=============================
Django Facebook photo api
=============================

.. image:: https://badge.fury.io/py/Django-Facebook-photo-api.svg
    :target: https://badge.fury.io/py/Django-Facebook-photo-api

.. image:: https://travis-ci.org/DmytroLitvinov/Django-Facebook-photo-api.svg?branch=master
    :target: https://travis-ci.org/DmytroLitvinov/Django-Facebook-photo-api

.. image:: https://codecov.io/gh/DmytroLitvinov/Django-Facebook-photo-api/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/DmytroLitvinov/Django-Facebook-photo-api

Get photos from Facebook by hashtags

Documentation
-------------

The full documentation is at https://Django-Facebook-photo-api.readthedocs.io.

Quickstart
----------

Install Django Facebook photo api::

    pip install Django-Facebook-photo-api

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_facebook_photo_api.apps.DjangoFacebookPhotoApiConfig',
        ...
    )

Add Django Facebook photo api's URL patterns:

.. code-block:: python

    from django_facebook_photo_api import urls as django_facebook_photo_api_urls


    urlpatterns = [
        ...
        url(r'^facebook_app/', include(django_twitter_photo_api_urls)),
        ...
    ]

Features
--------

* TODO

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
