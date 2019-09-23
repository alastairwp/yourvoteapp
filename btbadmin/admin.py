from django.contrib import admin
from .models import Location, Centre
from benchmark.models import Vote, Question, Hint, Category, SubCategory
from ptpadmin.models import Course, UserCourse


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]

    class Meta:
        Model = Category


class CentreAdmin(admin.ModelAdmin):
    list_display = ["name"]

    class Meta:
        Model = Centre


class CourseAdmin(admin.ModelAdmin):
    list_display = ["code", "title", "centre", "start_date"]

    class Meta:
        Model = Course


class HintAdmin(admin.ModelAdmin):
    list_display = ["question", "text", "position"]

    class Meta:
        Model = Hint


class LocationAdmin(admin.ModelAdmin):
    list_display = ["name"]

    class Meta:
        Model = Location


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["name", "number", "subcategory"]

    class Meta:
        Model = Question


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category"]

    class Meta:
        Model = SubCategory


class UserCourseAdmin(admin.ModelAdmin):
    list_display = ["user", "course", "status"]

    class Meta:
        Model = UserCourse


class VoteAdmin(admin.ModelAdmin):
    list_display = ["user", "value", "question", "comment_data", "course"]

    class Meta:
        Model = Vote


admin.site.register(Category, CategoryAdmin)
admin.site.register(Centre, CentreAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Hint, HintAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(UserCourse, UserCourseAdmin)
admin.site.register(Vote, VoteAdmin)