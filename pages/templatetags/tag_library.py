from django.utils.safestring import mark_safe
from django.template import Library

import json



register = Library()


@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))

@register.filter
def truncate_name(value, max_length=22):
    if len(value) > max_length:
        return value[:max_length] + '...'
    return value