from django.test import TestCase
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "muglaSepeti.settings")

import django

django.setup()
from django.utils import timezone


# def is_open(location, now=None):
#     """
#     Is the company currently open? Pass "now" to test with a specific
#     timestamp. Can be used stand-alone or as a helper.
#     """
#     if now is None:
#         now = get_now()
#
#     if has_closing_rule_for_now(location):
#         return False
#
#     now_time = datetime.time(now.hour, now.minute, now.second)
#
#     if location:
#         ohs = OpeningHours.objects.filter(company=location)
#     else:
#         ohs = Company.objects.first().openinghours_set.all()
#     for oh in ohs:
#         is_open = False
#         # start and end is on the same day
#         if (oh.weekday == now.isoweekday() and
#                 oh.from_hour <= now_time and
#                 now_time <= oh.to_hour):
#             is_open = oh
#
#         # start and end are not on the same day and we test on the start day
#         if (oh.weekday == now.isoweekday() and
#                 oh.from_hour <= now_time and
#                 ((oh.to_hour < oh.from_hour) and
#                     (now_time < datetime.time(23, 59, 59)))):
#             is_open = oh
#
#         # start and end are not on the same day and we test on the end day
#         if (oh.weekday == (now.isoweekday() - 1) % 7 and
#                 oh.from_hour >= now_time and
#                 oh.to_hour >= now_time and
#                 oh.to_hour < oh.from_hour):
#             is_open = oh
#             # print " 'Special' case after midnight", oh
#
#         if is_open is not False:
#             return oh
#     return False
# Create your tests here.
def get_is_open(open_at, close_at, current_time=timezone.localtime(timezone.now()).time()):
    if open_at > close_at:
        if open_at.hour >= 12:
            return open_at < current_time
        else:
            if close_at.hour >= 12:
                return close_at > current_time
            else:
                return close_at < current_time
    else:
        return open_at < current_time < close_at


def get_is_open2(open_at: timezone.datetime.time, close_at: timezone.datetime.time):
    current_time = timezone.localtime(timezone.now()).time()

    if open_at > close_at:
        return open_at < current_time < close_at


def test_get_is_open():
    for i in range(24):
        open_at = timezone.localtime(timezone.now() - timezone.timedelta(hours=i)).time()

        for j in range(24):

            close_at = timezone.localtime(timezone.now() + timezone.timedelta(hours=j)).time()
            for k in range(24):
                current_time = timezone.localtime(timezone.now() + timezone.timedelta(hours=k)).time()
                print(
                    f"opening:{open_at}|closing:{close_at}|current:{current_time}|result:{get_is_open(open_at, close_at, current_time)}")


test_get_is_open()
