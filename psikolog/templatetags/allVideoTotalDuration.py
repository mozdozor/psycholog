from django import template
from django.shortcuts import get_object_or_404
from Admin.models import CourseModel
import urllib
import json
from urllib.parse import urlparse,parse_qs



register=template.Library()


@register.simple_tag
def totalDurationOfCourse(pk):
    print("çalışıyor")
    totalMinutes=0
    totalSeconds=0
    course=get_object_or_404(CourseModel,pk=pk)
    for session in course.sessions.all():
        for video in session.videos.all():
            url_data = urlparse(video.url)
            query = parse_qs(url_data.query)
            videoId = query["v"][0]
            video_id=videoId
            api_key="AIzaSyD_CgkV7WTZL259eUsVCYeUsxWmXhHB_2c"
            searchUrl="https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&key="+api_key+"&part=contentDetails"
            response = urllib.request.urlopen(searchUrl).read()
            data = json.loads(response)
            all_data=data['items']
            contentDetails=all_data[0]['contentDetails']
            duration=contentDetails['duration']
            minutes = int(duration[2:].split('M')[0])
            seconds = int(duration[-3:-1])
            totalSeconds=totalSeconds+seconds+(60*minutes)
    totalMinutes=totalSeconds/60
    totalSeconds=totalSeconds%60
    strObject=str(totalMinutes)+":"+str(totalSeconds)
    return strObject
    

