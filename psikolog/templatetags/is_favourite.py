from django import template
from django.shortcuts import get_object_or_404

from Admin.models import CourseModel
from psikolog.models import favouriteCourseModel



register=template.Library()


@register.simple_tag
def isFavourite(request,pk):
    if request.user.is_authenticated:
        course=get_object_or_404(CourseModel,pk=pk)
        is_exist=favouriteCourseModel.objects.filter(user=request.user,course=course)
        if is_exist:
            return True
        else:
            return False
    return False

