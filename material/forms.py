from django.contrib.auth import get_user_model
from wagtail.users.forms import UserEditForm, UserCreationForm


class WagtailMonkeyPatchMixin:
    def __init__(self, *args, **kwargs):
        # Wagtail's UsernameForm.__init__ thinks we are using a "regular"
        # username field if its name is "username"
        User = get_user_model()
        old_username_field = User.USERNAME_FIELD
        User.USERNAME_FIELD = None
        super().__init__(*args, **kwargs)
        User.USERNAME_FIELD = old_username_field

        # XXX Another hack...
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False


# Used to work around https://github.com/wagtail/wagtail/issues/5924
class CustomUserEditForm(WagtailMonkeyPatchMixin, UserEditForm):
    class Meta(UserEditForm.Meta):
        fields = {'is_superuser', 'is_active', 'email', 'groups'}

    def separate_username_field(self):
        return False


class CustomUserCreationForm(WagtailMonkeyPatchMixin, UserCreationForm):
    class Meta(UserEditForm.Meta):
        fields = {'is_superuser', 'email', 'groups'}

    def separate_username_field(self):
        return False
