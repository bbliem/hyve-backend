#!/usr/bin/env python3
from material import models


cat1 = models.Category.objects.create(name_en="Category 1", description_en="Description of Category 1")
les1 = models.Lesson.objects.create(name_en="Lesson 1", description_en="Description of Lesson 1")
les2 = models.Lesson.objects.create(name_en="Lesson 2", description_en="Description of Lesson 2")
les3 = models.Lesson.objects.create(name_en="Lesson 3", description_en="Description of Lesson 3")
les4 = models.Lesson.objects.create(name_en="Lesson 4", description_en="Description of Lesson 4")
les5 = models.Lesson.objects.create(name_en="Lesson 5", description_en="Description of Lesson 5")
cat1.lessons.set([les1, les2, les3, les4, les5])

cat2 = models.Category.objects.create(name_en="Category 2", description_en="Description of Category 2")
les6 = models.Lesson.objects.create(name_en="Lesson 6", description_en="Description of Lesson 6")
cat2.lessons.set([les2, les6])

txt1 = models.Section.objects.create(text_en="foo")
txt2 = models.Section.objects.create(text_en="bar")
txt3 = models.Section.objects.create(text_en="baz")
qz1 = models.Section.objects.create()
q1 = models.Question.objects.create(text_en="Q?", section=qz1)
models.Answer.objects.create(question=q1, text_en="A1", correct=False, explanation_en="Explanation why A1 is false")
models.Answer.objects.create(question=q1, text_en="A2", correct=True, explanation_en="Explanation why A2 is true")
models.Content.objects.create(lesson=les1, section=txt1, page=1)
models.Content.objects.create(lesson=les1, section=qz1, page=1)
models.Content.objects.create(lesson=les1, section=txt2, page=2)
models.Content.objects.create(lesson=les1, section=txt3, page=3)

org1 = models.Organization.objects.create(name="Organization 1")
org1.lessons.set([les1])

org2 = models.Organization.objects.create(name="Organization 2")
org2.lessons.set([les2])

user1 = models.User.objects.create_superuser(email='foo@example.com', password='foobar123', name='Maija')
user2 = models.User.objects.create_user(email='bar@example.com', password='foobar123', name='Matti')

models.Membership.objects.create(user=user1, organization=org1, is_supervisor=False)
models.Membership.objects.create(user=user2, organization=org2, is_supervisor=True)

# Index page
models.StaticPage.objects.create(title_en='Hello', content_en='<p>Hello world</p>')
# About page
models.StaticPage.objects.create(title_en='About', content_en='<p>About this site...</p>')
