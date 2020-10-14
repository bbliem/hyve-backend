from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'categories'

    name = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.name


class Content(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class TextContent(Content):
    text = models.TextField()


class Quiz(Content):
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
