from django.contrib import admin

from .models import Answer, Category, Lesson, LessonContent, Quiz, Question, TextSection

admin.site.register(Category)
admin.site.register(Lesson)
admin.site.register(TextSection)
admin.site.register(LessonContent)


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionInline(admin.TabularInline):
    model = Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
