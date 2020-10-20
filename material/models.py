from django.db import models
from django.db.models import Q


class Lesson(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'categories'

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    lessons = models.ManyToManyField(Lesson)

    def __str__(self):
        return self.name


class TextSection(models.Model):
    text = models.TextField()


class Quiz(models.Model):
    class Meta:
        verbose_name_plural = 'quizzes'


class Question(models.Model):
    class Meta:
        order_with_respect_to = 'quiz'

    text = models.CharField(max_length=250)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Answer(models.Model):
    class Meta:
        order_with_respect_to = 'question'

    text = models.CharField(max_length=250)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class LessonContent(models.Model):
    # Make sure exactly one of the foreign keys to sections is null
    class Meta:
        # XOR isn't supported >:(
        _q_expr = ((Q(text_section__isnull=True) & Q(quiz__isnull=False))
                   | (Q(text_section__isnull=False) & Q(quiz__isnull=True)))
        _unique_fields = ['lesson', 'text_section', 'quiz']
        constraints = [
            models.CheckConstraint(check=_q_expr, name='exactly_one_section'),
            models.UniqueConstraint(fields=_unique_fields, name='no_duplicate_sections_per_lesson')
        ]

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    text_section = models.ForeignKey(TextSection, on_delete=models.CASCADE, blank=True, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, blank=True, null=True)

    page = models.PositiveIntegerField()
    order_on_page = models.PositiveIntegerField()
