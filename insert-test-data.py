#!/usr/bin/env python3
from material import models


cat1 = models.Category.objects.create(name="Category 1", description="Description of Category 1")
les1 = models.Lesson.objects.create(name="Lesson 1", description="Description of Lesson 1")
les2 = models.Lesson.objects.create(name="Lesson 2", description="Description of Lesson 2")
les3 = models.Lesson.objects.create(name="Lesson 3", description="Description of Lesson 3")
les4 = models.Lesson.objects.create(name="Lesson 4", description="Description of Lesson 4")
les5 = models.Lesson.objects.create(name="Lesson 5", description="Description of Lesson 5")
cat1.lessons.set([les1, les2, les3, les4, les5])

cat2 = models.Category.objects.create(name="Category 2", description="Description of Category 2")
les6 = models.Lesson.objects.create(name="Lesson 6", description="Description of Lesson 6")
cat2.lessons.set([les2, les6])

txt1 = models.Section.objects.create(text="foo")
txt2 = models.Section.objects.create(text="bar")
txt3 = models.Section.objects.create(text="baz")
qz1 = models.Section.objects.create()
q1 = models.Question.objects.create(text="Q?", section=qz1)
models.Answer.objects.create(question=q1, text="A1", correct=False)
models.Answer.objects.create(question=q1, text="A2", correct=True)
models.Content.objects.create(lesson=les1, section=txt1, page=1)
models.Content.objects.create(lesson=les1, section=qz1, page=1)
models.Content.objects.create(lesson=les1, section=txt2, page=2)
models.Content.objects.create(lesson=les1, section=txt3, page=3)

models.User.objects.create_superuser(email='foo@example.com', password='foobar123', name='Maija')
models.User.objects.create_user(email='bar@example.com', password='foobar123', name='Matti')

# Index page
models.StaticPage.objects.create(title='Hello', content='<p>Hello world</p>')
# About page
models.StaticPage.objects.create(title='About', content='<p>About this site...</p>')
