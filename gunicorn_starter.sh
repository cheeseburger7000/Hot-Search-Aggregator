#!/bin/sh

gunicorn  web_api:app -w 2 --threads 2 -b 0.0.0.0:8080
