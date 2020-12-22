from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from material import models

admin.site.register(models.Category)
admin.site.register(models.Organization)
admin.site.register(models.StaticPage)


class MultipleChoiceAnswerInline(admin.StackedInline):
    model = models.MultipleChoiceAnswer


@admin.register(models.MultipleChoiceQuestion)
class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    inlines = [MultipleChoiceAnswerInline]


class MultipleChoiceQuestionInline(admin.TabularInline):
    model = models.MultipleChoiceQuestion


class OpenQuestionInline(admin.TabularInline):
    model = models.OpenQuestion


@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
    inlines = [MultipleChoiceQuestionInline, OpenQuestionInline]


class ContentInline(admin.TabularInline):
    model = models.Content


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [ContentInline]


class SectionCompletionInline(admin.TabularInline):
    model = models.SectionCompletion


class MultipleChoiceResponseInline(admin.TabularInline):
    model = models.MultipleChoiceResponse


class OpenQuestionResponseInline(admin.TabularInline):
    model = models.OpenQuestionResponse


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    class Meta:
        model = models.User
        fields = ('email', 'organization')

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.User
        fields = ('email', 'organization', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'organization', 'name', 'is_supervisor', 'is_superuser')
    list_filter = ('organization', 'is_supervisor', 'is_superuser')
    readonly_fields = ('username',)
    fieldsets = (
        (None, {'fields': ('email', 'organization', 'username', 'password')}),
        ('Personal details', {'fields': ('name', 'avatar',)}),
        ('Permissions', {'fields': ('is_active', 'is_supervisor', 'is_superuser')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'organization', 'password1', 'password2', 'is_superuser'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    def get_inlines(self, request, obj):
        return [] if obj is None else [SectionCompletionInline, MultipleChoiceResponseInline, OpenQuestionResponseInline]


# Now register the new UserAdmin...
admin.site.register(models.User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
