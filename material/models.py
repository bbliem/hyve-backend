from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from material import managers


class Section(models.Model):
    """A section is part of a lesson and can be either a text or a quiz.

    Since the relational DB model cannot model polymorphism very well, we pack all possible fields into the same model.
    One alternative would be to use Django's generic foreign keys as described in
    https://stackoverflow.com/questions/933092/generic-many-to-many-relationships. However, this would require a lot
    of work to get usable in the Django admin, and it may be difficult for serialization. See, e.g.,
    https://stackoverflow.com/questions/13907211/genericforeignkey-and-admin-in-django
    """
    text = models.TextField()

    def __str__(self):
        preview = ''
        if self.text:
            preview = self.text
        elif self.questions:
            preview = self.questions.first().text
        # Merge whitespace
        preview = ' '.join(preview.split())
        s = f"Section {self.pk}"
        if preview:
            s += ': ' + preview[:50]
            if len(preview) > 50:
                s += '...'
        return s


class Question(models.Model):
    class Meta:
        order_with_respect_to = 'section'

    text = models.CharField(max_length=250)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.text


class Answer(models.Model):
    class Meta:
        order_with_respect_to = 'question'

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=250)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Lesson(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    sections = models.ManyToManyField(Section, through='Content')

    def __str__(self):
        return self.name


class Content(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['lesson', 'section'], name='no_duplicate_sections_per_lesson'),
        ]
        # TODO make sure page numbers respect the ordering relative to lesson
        order_with_respect_to = 'lesson'

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    page = models.PositiveIntegerField()


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'categories'

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    lessons = models.ManyToManyField(Lesson, blank=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=254,
        verbose_name='email address',
        unique=True,
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
        verbose_name='active',
    )
    # is_staff = models.BooleanField(
    #     default=False,
    #     help_text='Designates whether the user can log into this admin site.',
    #     verbose_name='staff status',
    # )
    is_admin = models.BooleanField(default=False)

    completed_sections = models.ManyToManyField(Section, blank=True)

    objects = managers.UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # TODO check if the following is a security problem
        return True

    def has_module_perms(self, app_label):
        # TODO check if the following is a security problem
        return True

    @property
    def is_staff(self):
        return self.is_admin
