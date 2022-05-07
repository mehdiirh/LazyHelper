from django.core.management.utils import get_random_secret_key

from pathlib import Path
import os
import re

BASE_DIR = Path(__file__).resolve().parent.parent
settings_path = os.path.join(BASE_DIR, 'LazyHelper/settings.py')

settings = open(settings_path, 'r').read()
start, end = re.search(r'SECRET_KEY = \'(.+)\'', settings).span(1)

secured_settings = f'{settings[:start]}SECURE///{get_random_secret_key()}{settings[end:]}'

with open(settings_path, 'w') as f:
    f.write(secured_settings)
