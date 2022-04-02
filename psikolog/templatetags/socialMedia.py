from django import template
from Admin.models import CourseModel, LogoModel, socialModel




register=template.Library()


@register.simple_tag
def getSocialMedia():
    return socialModel.objects.all().first()

