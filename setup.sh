#!/bin/bash

# Run this once before running django

#IMPORTANT: Be sure you are already in a virtualenv, otherwise the "pip" command
#below will be attempted system-wide!

python manage.py syncdb

mkdir sessions

pip install requirements.txt
