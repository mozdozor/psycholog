from django import template
from Admin.models import CourseModel




register=template.Library()


@register.simple_tag
def getStarCommentCount(number):
    return CourseModel.objects.filter(average_star=number).count()

