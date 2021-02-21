from wagtail.core import hooks
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import OpenQuestion, Organization, Quiz
from .choosers import OpenQuestionChooserViewSet, QuizChooserViewSet


@modeladmin_register
class OrganizationAdmin(ModelAdmin):
    model = Organization
    menu_icon = 'group'
    menu_order = 601
    add_to_settings_menu = True
    list_display = ('name', 'logo')
    search_filter = ('name',)


@modeladmin_register
class OpenQuestionAdmin(ModelAdmin):
    model = OpenQuestion
    menu_icon = 'edit'
    # menu_order = 601
    # list_display = ('name', 'logo')
    # search_filter = ('name',)


@modeladmin_register
class QuizAdmin(ModelAdmin):
    model = Quiz
    menu_icon = 'help'
    # menu_order = 601
    # list_display = ('name', 'logo')
    # search_filter = ('name',)


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
    menu_items[:] = [m for m in menu_items if m.name != 'reports']


@hooks.register('construct_settings_menu')
def hide_settings_menu_items(request, menu_items):
    HIDDEN_ITEMS = {
        'groups',
        'redirects',
        'sites',
        'workflow-tasks',
        'workflows',
        'groups',
        'sites',
    }
    menu_items[:] = [m for m in menu_items if m.name not in HIDDEN_ITEMS]


@hooks.register('construct_page_listing_buttons')
def hide_page_listing_buttons(buttons, page, page_perms, is_parent=False, context=None):
    buttons[:] = [b for b in buttons if b.label != "View live"]
