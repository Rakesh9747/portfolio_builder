#!/bin/bash
pip3 install -r requirements.txt --break-system-packages
python3.9 manage.py collectstatic --noinput
