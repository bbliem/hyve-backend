from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from .models import Category, Lesson, MultipleChoiceAnswer, MultipleChoiceQuestion, OpenQuestion, Quiz, StaticPage


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = (
        'description',
    )


@register(Lesson)
class LessonTranslationOptions(TranslationOptions):
    fields = (
        'description',
        'body',
    )


@register(StaticPage)
class StaticPageTranslationOptions(TranslationOptions):
    fields = (
        'body',
    )


# Due to bugs in wagtail-modeltranslation, we don't use it for quizzes
# @register(Quiz)
# class QuizTranslationOptions(TranslationOptions):
#     fields = (
#     )
# 
# 
# @register(MultipleChoiceQuestion)
# class MultipleChoiceQuestionTranslationOptions(TranslationOptions):
#     fields = (
#         'text',
#     )
# 
# 
# @register(MultipleChoiceAnswer)
# class MultipleChoiceAnswerTranslationOptions(TranslationOptions):
#     fields = (
#         'text',
#         'explanation',
#     )


@register(OpenQuestion)
class OpenQuestionTranslationOptions(TranslationOptions):
    fields = (
        'text',
    )
