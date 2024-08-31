# from django import template
# from django.utils.timesince import timesince

# register = template.Library()

# @register.filter
# def custom_timesince(value):
#     time_str = timesince(value)
#     # Check if the string contains 'day'
#     if 'day' in time_str:
#         return time_str.split(',')[0]  # Return only the day part
#     else:
#         # Split the time string and return just the hours part
#         return time_str.split(',')[0].split()[0] + ' hours'


from django import template
from django.utils.timesince import timesince
from datetime import datetime, timedelta
from django.utils import timezone

register = template.Library()

@register.filter
# def custom_timesince(date):
#     now = datetime.now()
#     diff = now - date

#     if diff < timedelta(days=1):
#         if diff < timedelta(hours=1):
#             minutes = diff.total_seconds() // 60
#             return f"{int(minutes)} minutes ago"
#         else:
#             hours = diff.total_seconds() // 3600
#             return f"{int(hours)} hours ago"
#     else:
#         return timesince(date) + " ago"


def custom_timesince(date):
    now = timezone.now()
    
    # Make sure both datetimes are timezone-aware
    if timezone.is_naive(date):
        date = timezone.make_aware(date, timezone.get_default_timezone())
    
    if date > now:
        return "In the future"

    diff = now - date

    if diff < timedelta(days=1):
        if diff < timedelta(hours=1):
            minutes = diff.total_seconds() // 60
            return f"{int(minutes)} minutes ago"
        else:
            hours = diff.total_seconds() // 3600
            return f"{int(hours)} hours ago"
    else:
        return timesince(date) + " ago"
