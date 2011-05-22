#!/bin/bash
export DJANGO_SETTINGS_MODULE=PROD_settings.py
PYTHONPATH=/work/django_src python manage.py runfcgi --settings=PROD_settings method=prefork host=127.0.0.1 port=3080
