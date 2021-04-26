import os
import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Q
from django_resized import ResizedImageField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.models import Orderable, Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel

from material import managers, storage
from material.blocks import OpenQuestionChooserBlock, QuizChooserBlock, MediaChooserBlock


def get_uuid_file_basename(filename):
    file_extension = os.path.splitext(filename)[1].lower()
    return f'{uuid.uuid4()}{file_extension}'


def get_avatar_file_path(instance, filename):
    return os.path.join('avatars', get_uuid_file_basename(filename))


def get_logo_file_path(instance, filename):
    file_extension = os.path.splitext(filename)[1].lower()
    basename = f'{instance.id}{file_extension}'
    return os.path.join('logos', basename)


class StaticPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    # parent_page_types = []
    subpage_types = []


class Lesson(Page):
    description = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField([
        ('lesson_content', blocks.RichTextBlock()),
        ('media', MediaChooserBlock()),
        ('quiz', QuizChooserBlock()),
        ('open_question', OpenQuestionChooserBlock()),
        ('page_break', blocks.StaticBlock()),
    ], blank=True)

    # FIXME: The following methods need to be kept in sync with the locales, which is terrible.
    @property
    def block_ids_en(self):
        return [block.id for block in self.body_en]

    @property
    def block_ids_fi(self):
        return [block.id for block in self.body_fi]

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
    ]

    parent_page_types = ['Category']
    subpage_types = []


class Quiz(ClusterableModel):
    class Meta:
        verbose_name_plural = 'quizzes'

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    internal_name = models.CharField(unique=True, max_length=250)
    # lesson = ParentalKey(Lesson, on_delete=models.CASCADE, related_name='quizzes')

    panels = [
        FieldPanel('internal_name'),
        MultiFieldPanel([
            InlinePanel('questions', label='Question', min_num=1),
        ], heading="Questions"),
    ]

    def __str__(self):
        return self.internal_name


class MultipleChoiceQuestion(Orderable, ClusterableModel):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = ParentalKey('Quiz', on_delete=models.CASCADE, related_name='questions')

    text_en = models.CharField(max_length=250, blank=True)
    text_fi = models.CharField(max_length=250, blank=True)

    panels = [
        FieldPanel('text_en'),
        FieldPanel('text_fi'),
        InlinePanel('answers', label='Answer', min_num=1),
    ]


class MultipleChoiceAnswer(Orderable):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = ParentalKey(MultipleChoiceQuestion, on_delete=models.CASCADE, related_name='answers')

    text_en = models.CharField(max_length=250, blank=True)
    text_fi = models.CharField(max_length=250, blank=True)
    correct = models.BooleanField(default=False)
    explanation_en = models.CharField(max_length=250, blank=True)
    explanation_fi = models.CharField(max_length=250, blank=True)

    panels = [
        FieldPanel('text_en'),
        FieldPanel('text_fi'),
        FieldPanel('correct'),
        FieldPanel('explanation_en'),
        FieldPanel('explanation_fi'),
    ]


class OpenQuestion(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # lesson = ParentalKey(Lesson, on_delete=models.CASCADE, related_name='open_questions')
    internal_name = models.CharField(unique=True, max_length=250)
    text = models.CharField(max_length=250, blank=True)

    panels = [
        FieldPanel('internal_name'),
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.internal_name


class Category(Page):
    class Meta:
        verbose_name_plural = 'categories'

    description = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        ImageChooserPanel('image'),
    ]

    parent_page_types = ['wagtailcore.page']
    subpage_types = ['Lesson']

    @property
    def lessons(self):
        return self.get_children().specific()


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True)
    lessons = models.ManyToManyField(Lesson, blank=True)
    logo = models.ImageField(blank=True,
                             storage=storage.OverwriteStorage(),
                             upload_to=get_logo_file_path)

    # URL of password reset form in frontend, returned when the user requests a link to reset their password.
    password_reset_url = models.CharField(max_length=250,
                                          blank=True,
                                          help_text="Include the patterns {uid}, {token} and, optionally, {language}.")

    panels = [
        FieldPanel('name'),
        FieldPanel('logo'),
        FieldPanel('lessons'),
        FieldPanel('password_reset_url'),
    ]

    def __str__(self):
        return str(self.name)


class User(PermissionsMixin, AbstractBaseUser):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email', 'organization'], name='no_duplicate_emails_per_organization'),
            models.CheckConstraint(check=Q(organization__isnull=False) | Q(is_superuser=True),
                                   name='admin_if_organization_is_null'),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=200, verbose_name='email address')
    # Organization should only be null for admin accounts; all others should have an organization
    organization = models.ForeignKey(Organization, blank=True, null=True, on_delete=models.CASCADE)
    # We want to identify users by the pair (email, organization). Unfortunately Django doesn't support composite
    # usernames. We therefore introduce a redundant field `username`, which is automatically set to a combination
    # of both fields.
    # XXX Currently manage.py createsuperuser asks for a username, but the value will be ignored and overwritten.
    username = models.CharField(max_length=254, unique=True)
    # first_name = models.CharField(max_length=100, blank=True)
    # last_name = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True)
    avatar = ResizedImageField(blank=True,
                               null=True,
                               storage=storage.OverwriteStorage(),
                               upload_to=get_avatar_file_path,
                               size=(400, 400),
                               quality=85,
                               keep_meta=False)
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be able to log in. Unselect this instead of deleting accounts.",
        verbose_name='active',
    )
    # Is this user a supervisor of their organization?
    is_supervisor = models.BooleanField(default=False,
                                        help_text="Designates whether this user should be able to manage data about "
                                                  "their organization and its members.",
                                        verbose_name="Organization supervisor")

    objects = managers.UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'organization']

    def __str__(self):
        return self.email if self.organization is None else f'{self.email} ({self.organization.name})'

    @property
    def is_staff(self):
        return self.is_superuser

    def has_module_perms(self, app_label):
        # TODO check if the following is a security problem
        return True

    def has_perm(self, perm, obj=None):
        # TODO check if the following is a security problem
        return True

    def save(self, *args, **kwargs):
        self.username = self.email
        if self.organization:
            self.username += f':{self.organization.id}'
        super().save(*args, **kwargs)


class BlockCompletion(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'block'], name='unique_completion_for_user_and_block'),
        ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    # Store the UUID of the StreamField block that was completed. This is not kept in sync with the StreamField, so if
    # the block is removed or the UUID changes, this model will contain obsolete values.
    block = models.UUIDField()
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
