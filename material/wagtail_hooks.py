from django.utils.translation import gettext_lazy as _
from wagtail.core import hooks
from wagtail.contrib.modeladmin.mixins import ThumbnailMixin
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import OpenQuestion, Organization, Quiz
from .choosers import OpenQuestionChooserViewSet, QuizChooserViewSet


@modeladmin_register
class OrganizationAdmin(ThumbnailMixin, ModelAdmin):
    model = Organization
    menu_icon = 'group'
    menu_order = 601
    add_to_settings_menu = True
    search_filter = ('name',)


@modeladmin_register
class OpenQuestionAdmin(ModelAdmin):
    model = OpenQuestion
    menu_icon = 'edit'


@modeladmin_register
class QuizAdmin(ModelAdmin):
    model = Quiz
    menu_icon = 'help'


@hooks.register('register_admin_viewset')
def register_quiz_chooser_viewset():
    return QuizChooserViewSet('quiz_chooser', url_prefix='quiz-chooser')


@hooks.register('register_admin_viewset')
def register_open_question_chooser_viewset():
    return OpenQuestionChooserViewSet('open_question_chooser', url_prefix='open-question-chooser')


@hooks.register('construct_page_action_menu')
def hide_page_action_menu_items(menu_items, request, context):
    HIDDEN_ITEMS = {
        # 'action-submit',  # "Submit to moderator's approval" -- removed by setting
        # WAGTAIL_MODERATION_ENABLED to False in settings
        'action-lock',
    }
    menu_items[:] = [m for m in menu_items if m.name not in HIDDEN_ITEMS]


@hooks.register('construct_page_action_menu')
def reorder_page_action_menu_items(menu_items, request, context):
    for index, item in enumerate(menu_items):
        if item.name == 'action-publish':
            menu_items.pop(index)
            menu_items.insert(0, item)
            break


@hooks.register('construct_main_menu')
def hide_main_menu_items(request, menu_items):
    # Just checking for `m.name` doesn't work because the name changes by locale
    menu_items[:] = [m for m in menu_items if m.__class__.__name__ != 'ReportsMenuItem']


@hooks.register('construct_settings_menu')
def hide_settings_menu_items(request, menu_items):
    HIDDEN_ITEMS = {
        'GroupsMenuItem',
        'RedirectsMenuItem',
        'SitesMenuItem',
        'WorkflowTasksMenuItem',
        'WorkflowsMenuItem',
        'GroupsMenuItem',
        'SitesMenuItem',
    }
    # Just checking for `m.name` doesn't work because the name changes by locale
    menu_items[:] = [m for m in menu_items if m.__class__.__name__ not in HIDDEN_ITEMS]


@hooks.register('construct_page_listing_buttons')
def hide_page_listing_buttons(buttons, page, page_perms, is_parent=False, context=None):
    buttons[:] = [b for b in buttons if b.label != _("View live")]
