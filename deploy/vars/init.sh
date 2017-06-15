#!/bin/bash
/root/integrates/manage.py makemigrations
/root/integrates/manage.py migrate
/root/integrates/manage.py runserver 0.0.0.0:8000 &
