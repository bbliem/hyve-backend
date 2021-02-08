from wagtail.core import blocks


class AnswerBlock(blocks.StructBlock):
    answer = blocks.CharBlock()
    correct = blocks.BooleanBlock(required=False)
    explanation = blocks.CharBlock(required=False)


class QuestionBlock(blocks.StructBlock):
    question = blocks.CharBlock()
    answers = blocks.ListBlock(AnswerBlock())


class QuizBlock(blocks.ListBlock):
    def __init__(self):
        return super().__init__(QuestionBlock())
