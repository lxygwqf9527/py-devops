# -*- coding:utf-8 -*-

from api.app import create_app
from api.extensions import celery

# celery worker -A celery_worker.celery -l DEBUG -E -Q devops_queue --concurrency=1

app = create_app()
app.app_context().push()
