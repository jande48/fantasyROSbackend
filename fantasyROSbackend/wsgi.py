"""
WSGI config for fantasyROSbackend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os, sys

# add the hellodjango project path into the sys.path
sys.path.append("/opt/FantasyROS/fantasyROSbackend")

# add the virtualenv site-packages path to the sys.path
sys.path.append("/opt/venv/Lib/site-packages")

# poiting to the project settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fantasyROSbackend.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()


# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fantasyROSbackend.settings')

# application = get_wsgi_application()
