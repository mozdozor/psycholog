from django.contrib import admin

from psikolog.models import CommentModel, CustomUserModel, billingCourseModel, favouriteCourseModel

# Register your models here.


admin.site.register(CustomUserModel)

admin.site.register(CommentModel)

admin.site.register(billingCourseModel)

admin.site.register(favouriteCourseModel)