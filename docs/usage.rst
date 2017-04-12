=====
Usage
=====

To use Django Facebook photo api in a project, add it to your `INSTALLED_APPS`:

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
        url(r'^', include(django_facebook_photo_api_urls)),
        ...
    ]
