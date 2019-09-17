from django import template
from django.contrib.auth.models import User
from signals.models import SignalTag

register = template.Library()


@register.filter
def get_users(users):

    return [u.username for u in User.objects.all()]


@register.filter
def get_tags(value):
    tags = [tag.name for tag in SignalTag.objects.all()]
    return tags


register.filter('get_tags', get_tags)
register.filter('get_users', get_users)
