from django import template
from Admin.models import CourseModel, LogoModel




register=template.Library()


@register.simple_tag
def getLogo():
    return LogoModel.objects.all().first()

