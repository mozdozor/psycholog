from django import template

from Admin.models import IletisimModel



register=template.Library()


@register.simple_tag
def new_messages():
    return IletisimModel.objects.filter(okundu_bilgisi="okunmadı").all()

