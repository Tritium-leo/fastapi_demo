from celery import Celery
from config import celeryconfig

app = Celery()
app.config_from_object(celeryconfig)