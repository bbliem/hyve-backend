#!/usr/bin/env python3
from django.db import transaction
from wagtail.core.models import Page

from material import models

with transaction.atomic():
    assert len(Page.get_root_nodes()) == 1
    root_page = Page.get_root_nodes()[0]
    assert len(root_page.get_children()) == 1
    site_page = root_page.get_children()[0]
    site_page.draft_title_en = "Material"
    site_page.draft_title_fi = "Materiaali"
    site_page.title_en = site_page.draft_title_en
    site_page.title_fi = site_page.draft_title_fi
    site_page.save()

    category = models.Category(title_en="Category",
                               title_fi="Kategoria",
                               description_en="Category description",
                               description_fi="Kategorian kuvaus")
    site_page.add_child(instance=category)
    lesson = models.Lesson(title_en="Lesson",
                           title_fi="Kappale",
                           description_en="Lesson description",
                           description_fi="Kappaleen kuvaus")
    category.add_child(instance=lesson)

    user1 = models.User.objects.create_superuser(email='foo@example.com',
                                                 password='foobar123',
                                                 name='Maija',
                                                 is_supervisor=False)

    organization = models.Organization.objects.create(id='5faabbd3-7203-4e74-a750-3608d3b80584',
                                                      name='Test organization',
                                                      password_reset_url='http://127.0.0.1:8080/password-reset/{uid}/{token}/')
    organization.lessons.set([lesson])

    static_page = models.StaticPage(title_en='Static page [en]',
                                    title_fi='Static page[fi]',
                                    body_en='<p>Body [en]</p>',
                                    body_fi='<p>Body [fi]</p>')
    root_page.add_child(instance=static_page)
