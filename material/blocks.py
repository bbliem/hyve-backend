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
