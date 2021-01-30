from wagtail.core import hooks

@hooks.register('construct_page_listing_buttons')
def hide_view_live_button(buttons, page, page_perms, is_parent=False, context=None):
    buttons[:] = [b for b in buttons if b.label != "View live"]
