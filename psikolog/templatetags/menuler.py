from django import template

from Admin.models import IletisimModel, topMenuModel



register=template.Library()


@register.simple_tag
def get_all_menus(request):
    if request.user.is_authenticated:
        return topMenuModel.objects.filter(userType="authUser").all().order_by("menuSira")
    return topMenuModel.objects.filter(userType="anonim").all().order_by("menuSira")

