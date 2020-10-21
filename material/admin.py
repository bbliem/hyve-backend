from django.contrib import admin

from .models import Answer, Category, Lesson, Question, Section, Content

admin.site.register(Category)


class AnswerInline(admin.TabularInline):
    model = Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


class QuestionInline(admin.TabularInline):
    model = Question


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


class ContentInline(admin.TabularInline):
    model = Content


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [ContentInline]
