# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u1625777/data/www/muhanjan.ru/muhanjan_loto')
sys.path.insert(1, '/var/www/u1625777/data/djangoenv/lib/python3.9/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'muhanjan_loto.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()