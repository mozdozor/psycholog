from django.contrib import admin

from Admin.models import CourseModel, IletisimModel, PageModel, bottomMenuModel, courseFeaturesModel, courseSessionModel, courseSessionVideoModel, notificationModel, topMenuModel

# Register your models here.


admin.site.register(IletisimModel)

admin.site.register(topMenuModel)

admin.site.register(bottomMenuModel)
admin.site.register(CourseModel)
admin.site.register(courseFeaturesModel)
admin.site.register(courseSessionModel)
admin.site.register(courseSessionVideoModel)
admin.site.register(PageModel)
admin.site.register(notificationModel)