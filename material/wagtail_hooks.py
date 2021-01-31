from wagtail.core import hooks


@hooks.register('construct_main_menu')
def hide_reports_menu_item(request, menu_items):
    menu_items[:] = [m for m in menu_items if m.name != 'reports']


@hooks.register('construct_settings_menu')
def hide_settings_submenu_items(request, menu_items):
    HIDDEN_ITEMS = [
        'redirects',
        'workflows',
        'workflow-tasks',
        'groups',
    ]
    menu_items[:] = [m for m in menu_items if m.name not in HIDDEN_ITEMS]


@hooks.register('construct_page_listing_buttons')
def hide_view_live_button(buttons, page, page_perms, is_parent=False, context=None):
    buttons[:] = [b for b in buttons if b.label != "View live"]
