import os

import celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = celery.Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
