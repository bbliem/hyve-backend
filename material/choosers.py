from generic_chooser.views import ModelChooserViewSet
from generic_chooser.widgets import AdminChooser

from .models import OpenQuestion, Quiz


class OpenQuestionChooserViewSet(ModelChooserViewSet):
    icon = 'help'
    model = OpenQuestion
    fields = ['internal_name']
    page_title = "Choose an open question"


class QuizChooserViewSet(ModelChooserViewSet):
    icon = 'help'
    model = Quiz
    fields = ['internal_name']
    page_title = "Choose a quiz"


class OpenQuestionChooser(AdminChooser):
    model = OpenQuestion
    choose_modal_url_name = 'open_question_chooser:choose'
    choose_one_text = "Choose an open question"
    choose_another_text = "Choose a different open question"


class QuizChooser(AdminChooser):
    model = Quiz
    choose_modal_url_name = 'quiz_chooser:choose'
    choose_one_text = "Choose a quiz"
    choose_another_text = "Choose a different quiz"
