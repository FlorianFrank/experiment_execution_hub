"""
Minimal file so Sphinx can work with Django for autodocumenting.

Location: /docs/django_settings.py
"""

# INSTALLED_APPS with these apps is necessary for Sphinx to build
# without warnings & errors
# Depending on your package, the list of apps may be different
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
]

SECRET_KEY = 'django-insecure-on_1t3+x!@xjd_ni3lhos^b8@^-p%ntfzo2u9n5705lm47)**-'
