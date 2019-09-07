from django.db import models


class Category(models.Model):
    name = models.CharField("Category Name", max_length=255, null=False, blank=False)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField("Sub-Category Name", max_length=255, null=False, blank=False)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = "Sub-categories"

    def __str__(self):
        return self.name


class Question(models.Model):
    name = models.TextField()
    number = models.PositiveIntegerField("Question number", default=0)
    subcategory = models.ForeignKey(SubCategory, null=True, on_delete=models.SET_NULL)


class Location(models.Model):
    name = models.CharField("Course location", max_length=50, null=False, blank=False)


class Course(models.Model):
    code = models.CharField("Course code", max_length=50, null=True, blank=True)
    title = models.CharField("Course title", max_length=255, null=False, blank=False)
    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
    start_date = models.DateField("Course start date", null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class Vote(models.Model):
    user = models.IntegerField()
    value = models.IntegerField()
    question = models.ForeignKey(Question, null=False, blank=False, on_delete=models.SET(0))
    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
    comment_data = models.TextField(max_length=1000)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class Hint(models.Model):
    question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL)
    text = models.CharField("Hint Text", max_length=255, null=False, blank=False)
    position = models.CharField("Hint Position", max_length=5, null=False, blank=False)


class UserCourse(models.Model):
    user = models.IntegerField()
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.PositiveIntegerField('Course status', default=0, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)







