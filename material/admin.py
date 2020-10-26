from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from material import models

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Category)


class AnswerInline(admin.TabularInline):
    model = models.Answer


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


class QuestionInline(admin.TabularInline):
    model = models.Question


@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


class ContentInline(admin.TabularInline):
    model = models.Content


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [ContentInline]
