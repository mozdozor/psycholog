from django import template
from Admin.models import CourseModel, LogoModel




register=template.Library()


@register.simple_tag
def getAdminLogo():
    return LogoModel.objects.all().first()

