from django.contrib import admin
from .models import Category, Hint, Question, SubCategory, Vote


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]

    class Meta:
        Model = Category


class HintAdmin(admin.ModelAdmin):
    list_display = ["question", "text", "position"]

    class Meta:
        Model = Hint


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["name", "number", "subcategory"]

    class Meta:
        Model = Question


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category"]

    class Meta:
        Model = SubCategory


class VoteAdmin(admin.ModelAdmin):
    list_display = ["user", "value", "question", "comment_data", "course"]

    class Meta:
        Model = Vote


admin.site.register(Category, CategoryAdmin)
admin.site.register(Hint, HintAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Vote, VoteAdmin)