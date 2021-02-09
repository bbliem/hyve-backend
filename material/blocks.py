from django.utils.functional import cached_property
from wagtail.core import blocks


class HiddenIdBlock(blocks.StaticBlock):
    """Add a hidden UUID to a (nested) StreamField block."""
    def value_from_datadict(self, data, files, prefix):
        return data['value'] or data['id']

    @cached_property
    def definition(self):
        definition = super().definition
        definition.update(html='', label='')
        return definition


class AnswerBlock(blocks.StructBlock):
    id = HiddenIdBlock()
    answer = blocks.CharBlock()
    correct = blocks.BooleanBlock(required=False)
    explanation = blocks.CharBlock(required=False)


class QuestionBlock(blocks.StructBlock):
    id = HiddenIdBlock()
    question = blocks.CharBlock()
    answers = blocks.ListBlock(AnswerBlock())


class QuizBlock(blocks.ListBlock):
    def __init__(self):
        return super().__init__(QuestionBlock())
