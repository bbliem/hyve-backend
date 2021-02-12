from django.utils.functional import cached_property
from wagtail.core import blocks


class ForceIdMixin:
    def prepare_value(self, value, errors=None):
        """
        Overwrite the ID of child blocks.

        This method is called when Wagtail creates the block for rendering. The value of the HiddenIdBlock called 'id',
        is the primary key of the model instance in the database that the block corresponds to. We set the ID to this
        value so that, when the form is submitted, we know which blocks refer to that model instance.

        This dirty hack probably breaks easily and depends on how wagtail-react-streamfield works at the moment.
        """
        prepared = super().prepare_value(value, errors)
        id_child_index = list(self.child_blocks).index('id')
        id_child = prepared[id_child_index]
        if id_child['value']:
            id_child['id'] = id_child['value']
        return prepared


class HiddenIdBlock(blocks.StaticBlock):
    """Add a hidden UUID to a (nested) StreamField block."""
    def value_from_datadict(self, data, files, prefix):
        """
        Return the PK of the row in the database that will be updated or created when saving the hierarchy.

        This is called when Wagtail serializes this block for saving.

        Ignore data['value'] and instead use data['id'] as the new value. It can be that data['value'] != data['id'],
        namely when a block was duplicated. Otherwise data['id'] would have been set to data['value'] at the time of the
        creation of this block for rendering in ForceIdMixin.
        """
        return data['id']

    @cached_property
    def definition(self):
        definition = super().definition
        definition.update(html='', label='')
        return definition


class AnswerBlock(ForceIdMixin, blocks.StructBlock):
    id = HiddenIdBlock()
    answer = blocks.CharBlock()
    correct = blocks.BooleanBlock(required=False)
    explanation = blocks.CharBlock(required=False)


class QuestionBlock(ForceIdMixin, blocks.StructBlock):
    id = HiddenIdBlock()
    question = blocks.CharBlock()
    answers = blocks.ListBlock(AnswerBlock())

    def value_from_datadict(self, data, files, prefix):
        """This is called when Wagtail serializes this block for saving."""
        return super().value_from_datadict(data, files, prefix)


class QuizBlock(ForceIdMixin, blocks.StructBlock):
    id = HiddenIdBlock()
    questions = blocks.ListBlock(QuestionBlock())
