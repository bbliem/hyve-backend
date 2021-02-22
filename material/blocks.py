from django.utils.functional import cached_property
from wagtail.core import blocks


class AnswerBlock(blocks.StructBlock):
    answer = blocks.CharBlock()
    correct = blocks.BooleanBlock(required=False)
    explanation = blocks.CharBlock(required=False)


class QuestionBlock(blocks.StructBlock):
    question = blocks.CharBlock()
    answers = blocks.ListBlock(AnswerBlock())

    def value_from_datadict(self, data, files, prefix):
        """This is called when Wagtail serializes this block for saving."""
        return super().value_from_datadict(data, files, prefix)


class QuizBlock(blocks.ListBlock):
    def __init__(self):
        return super().__init__(QuestionBlock())

    # def get_translatable_segments(*args, **kwargs):
    #     import pdb;pdb.set_trace()


class OpenQuestionChooserBlock(blocks.ChooserBlock):
    class Meta:
        icon = 'edit'

    @cached_property
    def target_model(self):
        from .models import OpenQuestion
        return OpenQuestion

    @cached_property
    def widget(self):
        from .choosers import OpenQuestionChooser
        return OpenQuestionChooser


class QuizChooserBlock(blocks.ChooserBlock):
    class Meta:
        icon = 'help'
        label = 'Quiz'

    @cached_property
    def target_model(self):
        from .models import Quiz
        return Quiz

    @cached_property
    def widget(self):
        from .choosers import QuizChooser
        return QuizChooser
