#!/usr/bin/env python3
from django.db import transaction
from wagtail.core.models import Page

from material import models

with transaction.atomic():
    assert len(Page.get_root_nodes()) == 1
    root_page = Page.get_root_nodes()[0]
    assert len(root_page.get_children()) == 1
    site_page = root_page.get_children()[0]
    site_page.draft_title = "Material"
    site_page.title = site_page.draft_title
    site_page.save()

    category = models.Category(title="Category")
    site_page.add_child(instance=category)
    lesson = models.Lesson(title="Lesson")
    category.add_child(instance=lesson)

    user1 = models.User.objects.create_superuser(email='foo@example.com',
                                                 password='foobar123',
                                                 name='Maija',
                                                 is_supervisor=False)
