from django import template
from Admin.models import CourseModel
import urllib
import json
from urllib.parse import urlparse,parse_qs



register=template.Library()


@register.simple_tag
def youtubeData(videoLink):
    url_data = urlparse(videoLink)
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
    strObject=str(minutes)+":"+str(seconds)
    return strObject

    

