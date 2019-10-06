from django.contrib import admin
from .models import Course, UserCentre, UserCourse


class CourseAdmin(admin.ModelAdmin):
    list_display = ["code", "title", "centre", "start_date"]

    class Meta:
        Model = Course


class UserCentreAdmin(admin.ModelAdmin):
    list_display = ["user", "centre"]

    class Meta:
        Model = UserCentre


class UserCourseAdmin(admin.ModelAdmin):
    list_display = ["user", "course", "status"]

    class Meta:
        Model = UserCourse


admin.site.register(Course, CourseAdmin)
admin.site.register(UserCentre, UserCentreAdmin)
admin.site.register(UserCourse, UserCourseAdmin)
