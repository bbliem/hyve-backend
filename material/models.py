import os
import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Q
from django_resized import ResizedImageField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.models import Orderable, Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.models import register_snippet

from material import managers
from material import storage


def get_uuid_file_basename(filename):
    file_extension = os.path.splitext(filename)[1].lower()
    return f'{uuid.uuid4()}{file_extension}'


def get_avatar_file_path(instance, filename):
    return os.path.join('avatars', get_uuid_file_basename(filename))


def get_logo_file_path(instance, filename):
    file_extension = os.path.splitext(filename)[1].lower()
    basename = f'{instance.id}{file_extension}'
    return os.path.join('logos', basename)


def get_video_file_path(instance, filename):
    return os.path.join('videos', get_uuid_file_basename(filename))


class StaticPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    # parent_page_types = []
    subpage_types = []


@register_snippet
class Quiz(ClusterableModel):
    class Meta:
        verbose_name_plural = 'quizzes'

    internal_name = models.CharField(max_length=250, blank=True)

    panels = [
        FieldPanel('internal_name'),
        MultiFieldPanel([
            InlinePanel('questions'),
        ], heading="Questions")
    ]

    def __str__(self):
        return self.internal_name


class MultipleChoiceQuestion(Orderable, ClusterableModel):
    quiz = ParentalKey('Quiz', on_delete=models.CASCADE, related_name='questions')

    text_en = models.CharField(max_length=250, blank=True)
    text_fi = models.CharField(max_length=250, blank=True)

    panels = [
        FieldPanel('text_en'),
        FieldPanel('text_fi'),
        MultiFieldPanel([
            InlinePanel('answers'),
        ], heading="Answers")
    ]


class MultipleChoiceAnswer(Orderable):
    question = ParentalKey(MultipleChoiceQuestion, on_delete=models.CASCADE, related_name='answers')

    text_en = models.CharField(max_length=250, blank=True)
    text_fi = models.CharField(max_length=250, blank=True)
    correct = models.BooleanField(default=False)
    explanation_en = models.CharField(max_length=250, blank=True)
    explanation_fi = models.CharField(max_length=250, blank=True)


@register_snippet
class OpenQuestion(models.Model):
    text_en = models.CharField(max_length=250, blank=True)
    text_fi = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.text_en or self.text_fi


class LessonPage(Page):
    description = RichTextField(blank=True)

    body = StreamField([
        ('lesson_content', blocks.RichTextBlock()),
        ('page_break', blocks.StaticBlock()),
        ('quiz', SnippetChooserBlock('material.Quiz')),
        ('open_question', SnippetChooserBlock('material.OpenQuestion')),
    ], blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        StreamFieldPanel('body'),
    ]

    parent_page_types = ['CategoryPage']
    subpage_types = []


class CategoryPage(Page):
    class Meta:
        verbose_name_plural = 'categories'

    description = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('description'),
    ]

    parent_page_types = ['wagtailcore.page']
    subpage_types = ['LessonPage']


@register_snippet
class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True)
    lessons = models.ManyToManyField(LessonPage, blank=True)
    logo = models.ImageField(blank=True,
                             storage=storage.OverwriteStorage(),
                             upload_to=get_logo_file_path)
    # URL of password reset form in frontend, returned when the user requests a link to reset their password.
    password_reset_url = models.CharField(max_length=250,
                                          blank=True,
                                          help_text="Include the patterns {uid}, {token} and, optionally, {language}.")

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

    # FIXME replace by something else
    # completed_sections = models.ManyToManyField(Section, blank=True, through='SectionCompletion')

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


# class SectionCompletion(models.Model):
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['user', 'section'], name='unique_completion_for_user_and_section'),
#         ]
#
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     section = models.ForeignKey(Section, on_delete=models.CASCADE)
#     last_modified = models.DateTimeField(auto_now=True)


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
