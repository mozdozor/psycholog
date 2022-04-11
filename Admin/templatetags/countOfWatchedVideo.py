from django import template
from django.shortcuts import get_object_or_404

from Admin.models import CustomUserModel,CourseModel
from psikolog.models import hasWatchedModel



register=template.Library()


@register.simple_tag
def getCountOfWatchedVideo(userId,courseId):
    user=get_object_or_404(CustomUserModel,pk=userId)
    course=get_object_or_404(CourseModel,pk=courseId)
    watchedVideoCount=0
    for watched in hasWatchedModel.objects.filter(user=user).all():
        if watched.video.courseSession.course == course:
            watchedVideoCount+=1

    return watchedVideoCount