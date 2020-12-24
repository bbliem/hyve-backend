from django.contrib.auth.management.commands import createsuperuser


class Command(createsuperuser.Command):
    """
    This terrible hack customizes the createsuperuser command because the built-in one can't deal with nullable
    foreign keys and also asks for a username even though in our case the username field is automatically generated
    from the email field.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username_field = self.UserModel._meta.get_field('email')

    def handle(self, *args, **options):
        original_required_fields = self.UserModel.REQUIRED_FIELDS
        self.UserModel.REQUIRED_FIELDS = [f for f in original_required_fields if f not in ('email', 'organization')]
        self.UserModel.USERNAME_FIELD = 'email'
        super().handle(*args, **options)
        self.UserModel.REQUIRED_FIELDS = original_required_fields
        self.UserModel.USERNAME_FIELD = 'username'
