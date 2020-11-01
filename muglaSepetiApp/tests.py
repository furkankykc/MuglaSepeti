from django.test import TestCase
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "muglaSepeti.settings")

import django
django.setup()
from django.utils import timezone


# Create your tests here.
def get_is_open(open_at, close_at):
    current_time = timezone.localtime(timezone.now()).time()

    if open_at > close_at:
        return open_at < current_time > close_at
    else:
        return open_at < current_time < close_at

    return False


def test_get_is_open():
    for i in range(24):
        open_at = timezone.localtime(timezone.now()- timezone.timedelta(hours=i)).time()
        close_at = timezone.localtime(timezone.now()+ timezone.timedelta(hours=i)).time()
        print(f"opening:{open_at}|closing:{close_at}|current:{timezone.localtime(timezone.now()).time()}result:{get_is_open(open_at, close_at)}")
test_get_is_open()