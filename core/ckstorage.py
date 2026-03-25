import os
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class CustomCKStorage(FileSystemStorage):
    FOLDER_NAME = "images"

    location = os.path.join(settings.MEDIA_ROOT, FOLDER_NAME)
    base_url = urljoin(settings.MEDIA_URL, f"{FOLDER_NAME}/")