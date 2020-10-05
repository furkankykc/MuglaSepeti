from django import template
from django.template.defaultfilters import stringfilter
from django.utils.translation import (
    gettext as _, gettext_lazy, ngettext, ngettext_lazy, npgettext_lazy,
    pgettext, round_away_from_one,
)

from django.template import defaultfilters
from django.utils.timezone import is_aware, utc
from datetime import date, datetime, timedelta

register = template.Library()


@register.filter
def modulo(num, val):
    return num % val


@register.filter
def subtract(num, val):
    return int(num) - val


@register.filter(is_safe=True)
@stringfilter
def ljusts(value, arg):
    """Left-align the value in a field of a given width."""
    return value.ljust(int(5 - int(arg)))


@register.filter(is_safe=True)
@stringfilter
def hiddenowner(value):
    return value[0] + '*' * (len(value) - 1)


@register.filter(is_safe=True)
@stringfilter
def quote(value):
    return "".join(value.split("-")[::-1])


@register.filter(is_safe=True)
@stringfilter
def lquote(value):
    return "".join(value.split("-")[-1])


@register.filter
def naturalduration(value):
    """
    For date and time values show how many seconds, minutes, or hours ago
    compared to current timestamp return representing string.
    """
    return NaturalDurationFormatter.string_for(value)


class NaturalDurationFormatter:
    time_strings = {
        # Translators: delta will contain a string like '2 months' or '1 month, 2 weeks'
        'past-day': gettext_lazy('%(delta)s ago'),
        # Translators: please keep a non-breaking space (U+00A0) between count
        # and time unit.
        'past-hour': ngettext_lazy('an hour ago', '%(count)s hours ago', 'count'),
        # Translators: please keep a non-breaking space (U+00A0) between count
        # and time unit.
        'past-minute': ngettext_lazy('a minute ago', '%(count)s minutes ago', 'count'),
        # Translators: please keep a non-breaking space (U+00A0) between count
        # and time unit.
        'past-second': ngettext_lazy('a second ago', '%(count)s seconds ago', 'count'),
        'now': gettext_lazy('now'),
        # Translators: please keep a non-breaking space (U+00A0) between count
        # and time unit.
        'future-second': ngettext_lazy('a second from now', '%(count)s seconds from now', 'count'),
        # Translators: please keep a non-breaking space (U+00A0) between count
        # and time unit.
        'future-minute': ngettext_lazy('a minute from now', '%(count)s minutes from now', 'count'),
        # Translators: please keep a non-breaking space (U+00A0) between count
        # and time unit.
        'future-hour': ngettext_lazy('an hour from now', '%(count)s hours from now', 'count'),
        # Translators: delta will contain a string like '2 months' or '1 month, 2 weeks'
        'future-day': gettext_lazy('%(delta)s from now'),
    }
    past_substrings = {
        # Translators: 'naturaltime-past' strings will be included in '%(delta)s ago'
        'year': npgettext_lazy('naturaltime-past', '%d year', '%d years'),
        'month': npgettext_lazy('naturaltime-past', '%d month', '%d months'),
        'week': npgettext_lazy('naturaltime-past', '%d week', '%d weeks'),
        'day': npgettext_lazy('naturaltime-past', '%d day', '%d days'),
        'hour': npgettext_lazy('naturaltime-past', '%d hour', '%d hours'),
        'minute': npgettext_lazy('naturaltime-past', '%d minute', '%d minutes'),
    }
    future_substrings = {
        # Translators: 'naturaltime-future' strings will be included in '%(delta)s from now'
        'year': npgettext_lazy('naturaltime-future', '%d year', '%d years'),
        'month': npgettext_lazy('naturaltime-future', '%d month', '%d months'),
        'week': npgettext_lazy('naturaltime-future', '%d week', '%d weeks'),
        'day': npgettext_lazy('naturaltime-future', '%d day', '%d days'),
        'hour': npgettext_lazy('naturaltime-future', '%d hour', '%d hours'),
        'minute': npgettext_lazy('naturaltime-future', '%d minute', '%d minutes'),
    }

    @classmethod
    def string_for(cls, value):
        if not isinstance(value, timedelta):  # datetime is a subclass of date
            return value

        delta = value
        if delta.seconds == 0:
            return cls.time_strings['now']
        elif delta.seconds < 60:
            return cls.time_strings['future-second'] % {'count': delta.seconds}
        elif delta.seconds // 60 < 60:
            count = delta.seconds // 60
            return cls.time_strings['future-minute'] % {'count': count}
        else:
            count = delta.seconds // 60 // 60
            return cls.time_strings['future-hour'] % {'count': count}
