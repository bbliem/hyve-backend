from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from material import managers


class StaticPage(models.Model):
    title_en = models.CharField(max_length=250, blank=True)
    title_fi = models.CharField(max_length=250, blank=True)
    content_en = models.TextField(blank=True)
    content_fi = models.TextField(blank=True)

    def __str__(self):
        return self.title_en or self.title_fi


class Section(models.Model):
    """A section is part of a lesson and can contain a text, multiple-choice questions or open questions.

    Since the relational DB model cannot model polymorphism very well, we pack all possible fields into the same model.
    One alternative would be to use Django's generic foreign keys as described in
    https://stackoverflow.com/questions/933092/generic-many-to-many-relationships. However, this would require a lot
    of work to get usable in the Django admin, and it may be difficult for serialization. See, e.g.,
    https://stackoverflow.com/questions/13907211/genericforeignkey-and-admin-in-django
    """
    text_en = models.TextField(blank=True)
    text_fi = models.TextField(blank=True)

    def __str__(self):
        preview = ''
        if self.text_en:
            preview = self.text_en
        elif self.multiple_choice_questions:
            preview = self.multiple_choice_questions.first().text_en
        elif self.open_questions:
            preview = self.open_questions.first().text_en
        # Merge whitespace
        preview = ' '.join(preview.split())
        s = f"Section {self.pk}"
        if preview:
            s += ': ' + preview[:50]
            if len(preview) > 50:
                s += '...'
        return s


class MultipleChoiceQuestion(models.Model):
    class Meta:
        order_with_respect_to = 'section'

    text_en = models.CharField(max_length=250, blank=True)
    text_fi = models.CharField(max_length=250, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='multiple_choice_questions')

    def __str__(self):
        return self.text_en or self.text_fi


class MultipleChoiceAnswer(models.Model):
    class Meta:
        order_with_respect_to = 'question'

    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE, related_name='answers')
    text_en = models.CharField(max_length=250, blank=True)
    text_fi = models.CharField(max_length=250, blank=True)
    correct = models.BooleanField(default=False)
    explanation_en = models.CharField(max_length=250, blank=True)
    explanation_fi = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.text_en or self.text_fi


class OpenQuestion(models.Model):
    class Meta:
        order_with_respect_to = 'section'

    text_en = models.CharField(max_length=250, blank=True)
    text_fi = models.CharField(max_length=250, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='open_questions')

    def __str__(self):
        return self.text_en or self.text_fi


class Lesson(models.Model):
    name_en = models.CharField(max_length=150, blank=True)
    name_fi = models.CharField(max_length=150, blank=True)
    description_en = models.TextField(blank=True)
    description_fi = models.TextField(blank=True)
    sections = models.ManyToManyField(Section, through='Content')

    def __str__(self):
        return self.name_en or self.name_fi


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

    name_en = models.CharField(max_length=150, blank=True)
    name_fi = models.CharField(max_length=150, blank=True)
    description_en = models.TextField(blank=True)
    description_fi = models.TextField(blank=True)
    lessons = models.ManyToManyField(Lesson, blank=True, related_name='categories')

    def __str__(self):
        return self.name_en or self.name_fi


class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=254,
        verbose_name='email address',
        unique=True,
    )
    name = models.CharField(max_length=100, blank=True)
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
    is_superuser = models.BooleanField(default=False)

    completed_sections = models.ManyToManyField(Section, blank=True, through='SectionCompletion')

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
        return self.is_superuser


class SectionCompletion(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'section'], name='unique_completion_for_user_and_section'),
        ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)


class MultipleChoiceResponse(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'answer'], name='unique_response_for_user_and_answer'),
        ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(MultipleChoiceAnswer, on_delete=models.CASCADE)
    response = models.BooleanField()
    last_modified = models.DateTimeField(auto_now=True)


class OpenQuestionResponse(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'question'], name='unique_response_for_user_and_question'),
        ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(OpenQuestion, on_delete=models.CASCADE)
    response = models.TextField()
    last_modified = models.DateTimeField(auto_now=True)


class Organization(models.Model):
    name = models.CharField(max_length=100, blank=True)
    users = models.ManyToManyField(User, through='Membership')
    lessons = models.ManyToManyField(Lesson)

    def __str__(self):
        return self.name


class Membership(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'organization'], name='no_duplicate_user_per_organization'),
        ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    is_supervisor = models.BooleanField(default=False)
