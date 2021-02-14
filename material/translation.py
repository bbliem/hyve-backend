from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from .models import Category, Lesson, StaticPage


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
