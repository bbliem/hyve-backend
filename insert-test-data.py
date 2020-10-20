#!/usr/bin/env python3
from material import models


cat1 = models.Category.objects.create(name="Category 1")
les1 = models.Lesson.objects.create(name="Lesson 1")
cat1.lessons.set([les1])
txt1 = models.TextSection.objects.create(text="foo")
qz1 = models.Quiz.objects.create()
models.LessonContent.objects.create(lesson=les1, text_section=txt1, page=1, order_on_page=1)
models.LessonContent.objects.create(lesson=les1, quiz=qz1, page=1, order_on_page=2)
