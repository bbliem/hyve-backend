import os
import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models, transaction
from django.db.models import Q
from django_resized import ResizedImageField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.models import Orderable, Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail_localize.fields import BaseTranslatableField
from wagtailvideos.blocks import VideoChooserBlock

from material import managers, storage
from material.blocks import QuizBlock


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


class SyncedChildModelsMixin:
    """
    Sync data of an instance and its descendants (in some hierarchy) with StreamField blocks.

    When you use this mixin, your class should implement `sync`. This method should update the instance itself. If the
    model has children to sync, the class body must contain a list of instances of SyncedChildModel called
    `synced_child_models`.

    The child model must (probably?) be linked to the parent with a ParentalKey and the parent must extend
    ClusterableModel.
    """
    synced_child_models = []

    def sync_hierarchy(self, block):
        self.sync(block)
        for synced_child_model in self.synced_child_models:
            self.sync_child_model(synced_child_model, block)

    def sync_child_model(self, model, block):
        child_blocks = block[model.blocks_key]
        child_instances = getattr(self, model.instances_field)

        child_blocks_by_id = {uuid.UUID(b['id']): b for b in child_blocks}
        new_child_ids = set(child_blocks_by_id.keys())
        # UUID(str(id)) because id can be either a string or a UUID
        old_child_ids = set(uuid.UUID(str(id)) for id in child_instances.values_list('id', flat=True) if id is not None)

        # Delete children
        for child_id in old_child_ids - new_child_ids:
            child = child_instances.model.objects.get(id=child_id)
            # child.delete()
            # Use modelcluster functionality instead. Deletion is done when the root is saved.
            child_instances.remove(child)
            # FIXME: For some reason I haven't figured out yet, the IDs handled by modelcluster are sometimes strings,
            # sometimes UUIDs, and if they are strings the previous call to remove() will not have done anything.
            child.id = str(child.id)
            child_instances.remove(child)

        # Update children
        for child_id in old_child_ids & new_child_ids:
            # child = child_instances.get(id=child_id)
            # For some reason this doesn't work with `id`.
            child = child_instances.model.objects.get(id=child_id)
            child.sync_hierarchy(child_blocks_by_id[child_id])
            # Node that we need to "add" the child even though it is already there. Otherwise the changes will
            # not be saved. django-modelcluster treats adding already existing children as an update. Hopefully
            # this stays so in the future.
            child_instances.add(child)

        # Create children
        for child_id in new_child_ids - old_child_ids:
            child = child_instances.model(id=child_id)
            child.sync_hierarchy(child_blocks_by_id[child_id])
            child_instances.add(child)


class SyncedChildModel:
    """
    Use instances of this class in a list called `synced_child_models` in the definitions of each class that extends
    SyncedChildModelsMixin and has child models to sync. For each synced child model of that class, you must put one
    instance in the list.
    """
    def __init__(self, instances_field, blocks_key=None):
        """
        `instances_field` is the name of the model field containing the child model instances to be synced. `blocks_key`
        is the key of the StreamField block dict for getting the child blocks. If `blocks_key` is None, it will be set
        to `instances_field`.
        """
        self.instances_field = instances_field
        if blocks_key is None:
            self.blocks_key = instances_field
        else:
            self.blocks_key = blocks_key


class StaticPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    # parent_page_types = []
    subpage_types = []


class NonEditableField(BaseTranslatableField):
    # Marking a field as non-editable entails that wagtail_localize doesn't synchronize it, which is what we want for,
    # e.g., the child model instances of Quiz, because we want wagtail_localize to ignore them as they are generated
    # from `body`, which is synchronized.
    def is_editable(self, obj):
        """
        Returns True if the field is editable on the given object
        """
        return False


class Lesson(SyncedChildModelsMixin, Page):
    synced_child_models = [
        SyncedChildModel('quizzes'),
        SyncedChildModel('open_questions'),
    ]

    override_translatable_fields = [
        NonEditableField('quizzes'),
        NonEditableField('open_questions'),
    ]

    description = RichTextField(blank=True)

    body = StreamField([
        ('lesson_content', blocks.RichTextBlock()),
        ('video', VideoChooserBlock()),
        ('page_break', blocks.StaticBlock()),
        ('quiz', QuizBlock()),
        ('open_question', blocks.RichTextBlock()),
    ], blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        StreamFieldPanel('body'),
    ]

    parent_page_types = ['Category']
    subpage_types = []

    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields')
        if update_fields and 'body' not in update_fields:
            # This update doesn't change body, so we don't do anything
            super().save(*args, **kwargs)
        else:
            # Sync child models
            import pdb;pdb.set_trace()
            data = {
                'quizzes': [block['value'] for block in self.body.stream_data if block['type'] == 'quiz'],
                'open_questions': [block for block in self.body.stream_data if block['type'] == 'open_question'],
            }
            self.sync_hierarchy(data)
            super().save(*args, **kwargs)

    def sync(self, block):
        pass

    def copy_all_child_relations(self, target, *args, **kwargs):
        # TODO: Make this generic.
        # Called when, e.g., a copy (rather, an alias) for a new translation is made.
        # Add child models to excluded fields to avoid creating instances of them that would then be created by save()
        kwargs['exclude'] = kwargs.get('exclude', [])
        for child_model in self.synced_child_models:
            kwargs['exclude'].append(child_model.instances_field)
        # # Update IDs in target, otherwise we'd later create child model instances with duplicate PKs
        target.reset_body_ids()
        import pdb;pdb.set_trace()
        # TODO copy body here?
        from wagtail.core.blocks.stream_block import StreamValue
        target.body = StreamValue(self.body.stream_block,
                                  self.body.stream_data,
                                  is_lazy=self.body.is_lazy,
                                  raw_text=self.body.raw_text)
        return super().copy_all_child_relations(target, *args, **kwargs)

    @transaction.atomic
    def copy_child_relation(self, child_relation, target, commit=False, append=False):
        import pdb;pdb.set_trace()
        child_object_map = super().copy_child_relation(child_relation, target, commit, append)
        # OLD: super().copy_child_relation() has removed the PK of the child. Set it to a new UUID and update it in the body.
        # super().copy_child_relation() has removed the PK of the child.
        # Leave it as None, but set a new UUID in the body.
        # FIXME: Make generic.
        for (_, old_pk), child_object in child_object_map.items():
            new_id = str(uuid.uuid4())
            # child_object.id = new_id
            if child_relation.name == 'quizzes':
                for value in (block['value'] for block in target.body.stream_data if block['type'] == 'quiz'):
                    value['id'] = new_id
            # TODO: 'open_questions'
        return child_object_map

    def reset_body_ids(self):
        """Set IDs in the body blocks of the entire synced child model hierarchy to new UUIDs."""
        # FIXME: Make this terrible code generic. Keep in mind that we may not have synced child model instances yet
        # even though there might be blocks for them in the body.
        for block in self.body.stream_data:
            if block['type'] == 'quiz':
                # block['id'] = str(uuid.uuid4())  # Actually this is not a synced child block, so commented out...
                block['value']['id'] = str(uuid.uuid4())
                for question_block in block['value']['questions']:
                    question_block['id'] = str(uuid.uuid4())
                    for answer_block in question_block['answers']:
                        answer_block['id'] = str(uuid.uuid4())
            elif block['type'] == 'open_question':
                block['id'] = str(uuid.uuid4())


class Quiz(SyncedChildModelsMixin, ClusterableModel):
    class Meta:
        # Or better...? class Meta(ClusterableModel.Meta):
        verbose_name_plural = 'quizzes'
        # unique_together = [('translation_key', 'locale')]

    synced_child_models = [
        SyncedChildModel('questions'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = ParentalKey(Lesson, on_delete=models.CASCADE, related_name='quizzes')

    panels = [
        FieldPanel('lesson'),
        MultiFieldPanel([
            InlinePanel('questions'),
        ], heading="Questions")
    ]

    def sync(self, block):
        pass


# TODO: We can get rid of Orderable since the ordering is done in the StreamField.
class MultipleChoiceQuestion(SyncedChildModelsMixin, Orderable, ClusterableModel):
    synced_child_models = [
        SyncedChildModel('answers'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = ParentalKey('Quiz', on_delete=models.CASCADE, related_name='questions')

    text = models.CharField(max_length=250, blank=True)

    panels = [
        FieldPanel('text'),
        MultiFieldPanel([
            InlinePanel('answers'),
        ], heading="Answers")
    ]

    def sync(self, block):
        assert self.id == uuid.UUID(block['id'])
        self.text = block['question']


# TODO: We can get rid of Orderable since the ordering is done in the StreamField.
class MultipleChoiceAnswer(SyncedChildModelsMixin, Orderable):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = ParentalKey(MultipleChoiceQuestion, on_delete=models.CASCADE, related_name='answers')

    text = models.CharField(max_length=250, blank=True)
    correct = models.BooleanField(default=False)
    explanation = models.CharField(max_length=250, blank=True)

    def sync(self, block):
        assert self.id == uuid.UUID(block['id'])
        self.text = block['answer']
        self.correct = block['correct']
        self.explanation = block['explanation']


class OpenQuestion(models.Model):
    lesson = ParentalKey(Lesson, on_delete=models.CASCADE, related_name='open_questions')
    text = models.CharField(max_length=250, blank=True)


class Category(Page):
    class Meta:
        verbose_name_plural = 'categories'

    description = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('description'),
    ]

    parent_page_types = ['wagtailcore.page']
    subpage_types = ['Lesson']


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
        InlinePanel('lessons'),
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
