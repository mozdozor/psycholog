from django import template

from Admin.models import IletisimModel, notificationModel



register=template.Library()


@register.simple_tag
def new_notifications():
    return notificationModel.objects.filter(has_readen="no").all()

