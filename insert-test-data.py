#!/usr/bin/env python3
from material import models


cat1 = models.Category.objects.create(name="Category 1")
les1 = models.Lesson.objects.create(name="Lesson 1")
les2 = models.Lesson.objects.create(name="Lesson 2")
cat1.lessons.set([les1, les2])

cat2 = models.Category.objects.create(name="Category 2")
les3 = models.Lesson.objects.create(name="Lesson 3")
cat2.lessons.set([les2, les3])

txt1 = models.Section.objects.create(text="foo")
txt2 = models.Section.objects.create(text="bar")
qz1 = models.Section.objects.create()
q1 = models.Question.objects.create(text="Q?", section=qz1)
models.Answer.objects.create(question=q1, text="A1", correct=False)
models.Answer.objects.create(question=q1, text="A2", correct=True)
models.Content.objects.create(lesson=les1, section=txt1, page=1)
models.Content.objects.create(lesson=les1, section=qz1, page=1)
models.Content.objects.create(lesson=les1, section=txt2, page=2)
