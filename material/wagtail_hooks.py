from wagtail.core import hooks


@hooks.register('construct_page_action_menu')
def hide_page_action_menu_items(menu_items, request, context):
    HIDDEN_ITEMS = [
        'action-submit',  # "Submit to moderator's approval"
        'action-lock',
    ]
    menu_items[:] = [m for m in menu_items if m.name not in HIDDEN_ITEMS]


@hooks.register('construct_main_menu')
def hide_main_menu_items(request, menu_items):
    menu_items[:] = [m for m in menu_items if m.name != 'reports']


@hooks.register('construct_settings_menu')
def hide_settings_menu_items(request, menu_items):
    HIDDEN_ITEMS = [
        'redirects',
        'workflows',
        'workflow-tasks',
        'groups',
    ]
    menu_items[:] = [m for m in menu_items if m.name not in HIDDEN_ITEMS]


@hooks.register('construct_page_listing_buttons')
def hide_page_listing_buttons(buttons, page, page_perms, is_parent=False, context=None):
    buttons[:] = [b for b in buttons if b.label != "View live"]
