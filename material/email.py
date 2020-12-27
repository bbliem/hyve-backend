from django.contrib.auth.tokens import default_token_generator
from djoser import utils
from templated_mail.mail import BaseEmailMessage


class PasswordResetEmail(BaseEmailMessage):
    template_name = "email/password_reset.html"

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get('user')
        context['uid'] = utils.encode_uid(user.pk)
        context['token'] = default_token_generator.make_token(user)
        context['url'] = user.organization.password_reset_url.format(**context)
        return context
