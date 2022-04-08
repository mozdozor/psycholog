from django.contrib import admin

from Admin.models import CategoryModel, CourseModel, IletisimModel, LogoModel, PageModel, aydinlatmaMetniModel, bottomMenuModel, courseFeaturesModel, courseSessionModel, courseSessionVideoModel, gizlilikMetniModel, kvkkMetniModel, mesafeliSatisModel, notificationModel, topMenuModel, whatWillYouLearnModel

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
admin.site.register(CategoryModel)
admin.site.register(whatWillYouLearnModel)
admin.site.register(LogoModel)
admin.site.register(mesafeliSatisModel)
admin.site.register(kvkkMetniModel)
admin.site.register(aydinlatmaMetniModel)
admin.site.register(gizlilikMetniModel)