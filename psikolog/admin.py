from django.contrib import admin

from psikolog.models import CommentModel, CustomUserModel, billingCourseModel, favouriteCourseModel, orderModel, sliderModel
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.register(CommentModel)

admin.site.register(billingCourseModel)

admin.site.register(favouriteCourseModel)
admin.site.register(sliderModel)

admin.site.register(orderModel)




@admin.register(CustomUserModel)
class CustomUserAdmin(UserAdmin):
    readonly_fields = [
        'date_joined',
    ]