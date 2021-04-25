from django.forms.utils import flatatt
from django.utils.functional import cached_property
from django.utils.html import format_html, format_html_join
from wagtail.core import blocks
from wagtailmedia.blocks import AbstractMediaChooserBlock


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


class MediaChooserBlock(AbstractMediaChooserBlock):
    class Meta:
        icon = 'media'

    def get_api_representation(self, value, context):
        request = context['request']
        if value.thumbnail:
            thumbnail_url = request.build_absolute_uri(value.thumbnail.url)
        else:
            thumbnail_url = None
        return {
            'type': value.type,
            'file': request.build_absolute_uri(value.file.url),
            'width': value.width,
            'height': value.height,
            'thumbnail': thumbnail_url,
        }

    def render_basic(self, value, context=None):
        if not value:
            return ''

        if value.type == 'video':
            player_code = '''
            <div>
                <video width="320" height="240" controls>
                    {0}
                    Your browser does not support the video tag.
                </video>
            </div>
            '''
        else:
            player_code = '''
            <div>
                <audio controls>
                    {0}
                    Your browser does not support the audio element.
                </audio>
            </div>
            '''

        return format_html(player_code, format_html_join(
            '\n', "<source{0}>",
            [[flatatt(s)] for s in value.sources]
        ))
