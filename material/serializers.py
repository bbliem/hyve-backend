from drf_base64.serializers import ModelSerializer as Base64ModelSerializer
from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers

from material import models


class StaticPageSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.StaticPage
        fields = ['url', 'id', 'title_en', 'title_fi', 'body_en', 'body_fi']


class MultipleChoiceAnswerSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.MultipleChoiceAnswer
        fields = ['url', 'id', 'question', 'text_en', 'text_fi', 'correct', 'explanation_en', 'explanation_fi']


class MultipleChoiceQuestionSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.MultipleChoiceQuestion
        fields = ['url', 'id', 'text_en', 'text_fi', 'answers']
        expandable_fields = {
            'answers': (MultipleChoiceAnswerSerializer, {'source': 'answers', 'many': True, 'omit': ['question']})
        }


class QuizSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Quiz
        fields = ['url', 'id', 'questions']
        expandable_fields = {
            'questions': (MultipleChoiceQuestionSerializer, {'many': True})
        }


class OpenQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OpenQuestion
        fields = ['url', 'id', 'text_en', 'text_fi']


class LessonSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = ['url', 'id', 'title_en', 'title_fi', 'description_en', 'description_fi', 'body_en', 'body_fi',
                  'block_ids_en', 'block_ids_fi', 'videos_en', 'videos_fi']
        # expandable_fields = {
        #     'contents': (ContentSerializer, {'source': 'content_set', 'many': True, 'omit': ['lesson']})
        # }


class CategorySerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['url', 'id', 'title_en', 'title_fi', 'description_en', 'description_fi', 'lessons']
        expandable_fields = {
            'lessons': (LessonSerializer, {'many': True, 'source': 'lessons'})
        }

    lessons = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


class BlockCompletionSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.BlockCompletion
        fields = ['url', 'id', 'user', 'lesson', 'block', 'last_modified']

    def validate_user(self, value):
        if value != self.context['request'].user:
            raise serializers.ValidationError("User specified in BlockCompletion object is not yourself")
        return value


class MultipleChoiceResponseSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.MultipleChoiceResponse
        fields = ['url', 'id', 'user', 'answer', 'response', 'last_modified']

    def validate_user(self, value):
        if value != self.context['request'].user:
            raise serializers.ValidationError("User specified in MultipleChoiceResponse object is not yourself")
        return value


class OpenQuestionResponseSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.OpenQuestionResponse
        fields = ['url', 'id', 'user', 'question', 'response', 'last_modified']

    def validate_user(self, value):
        if value != self.context['request'].user:
            raise serializers.ValidationError("User specified in OpenQuestionResponse object is not yourself")
        return value


class OrganizationSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    """
    Serializer for the Organization model that does not include information about members.

    We deliberately don't include the organization's users in the (expandable) fields because only supervisors should
    see those. If you have made sure that the accessing user is a supervisor, you can use
    OrganizationSerializerWithMembers instead to get all the information.
    """
    class Meta:
        model = models.Organization
        fields = ['url', 'id', 'name', 'lessons']
        expandable_fields = {
            'lessons': (LessonSerializer, {'source': 'lessons', 'many': True}),
        }

    lessons = LessonSerializer(many=True, read_only=True, omit=['body_en', 'body_fi'])


class OrganizationSerializerWithMembers(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    """
    Serializer for the Organization model including data about the organization members.
    """
    class Meta:
        model = models.Organization
        fields = ['url', 'id', 'name', 'lessons']
        expandable_fields = {
            # 'lessons': (LessonSerializer, {'source': 'lessons', 'many': True}),
            'users': ('material.UserSerializer', {'source': 'user_set', 'many': True, 'omit': ['organization']})
        }


class OrganizationSerializerWithSupervisors(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    """
    Serializer for the Organization model including data about the organization supervisors.
    """
    class Meta:
        model = models.Organization
        fields = ['url', 'id', 'name', 'lessons']
        expandable_fields = {
            # 'lessons': (LessonSerializer, {'source': 'lessons', 'many': True}),
            'users': ('material.SupervisorSerializer', {'source': 'user_set', 'many': True, 'omit': ['organization']})
        }


class UserSerializer(FlexFieldsSerializerMixin, Base64ModelSerializer):
    class Meta:
        model = models.User
        fields = ['url', 'id', 'email', 'organization', 'username', 'name', 'avatar', 'is_supervisor', 'is_superuser']
        read_only_fields = ['is_supervisor', 'is_superuser']
        expandable_fields = {
            'organization': OrganizationSerializer,
            'block_completions': (BlockCompletionSerializer, {'source': 'blockcompletion_set', 'many': True, 'omit': ['user']}),
            'multiple_choice_responses': (MultipleChoiceResponseSerializer, {'source': 'multiplechoiceresponse_set', 'many': True, 'omit': ['user']}),
            'open_question_responses': (OpenQuestionResponseSerializer, {'source': 'openquestionresponse_set', 'many': True, 'omit': ['user']}),
        }

    def update(self, instance, validated_data):
        # Do not allow updating the organization
        validated_data.pop('organization', None)
        return super().update(instance, validated_data)


class SupervisorListSerializer(serializers.ListSerializer):
    """Serializes models (such as User) that have an `is_supervisor` field"""
    # https://stackoverflow.com/questions/28163556/how-do-you-filter-a-nested-serializer-in-django-rest-framework
    def to_representation(self, data):
        data = data.filter(is_supervisor=True)
        return super().to_representation(data)


class SupervisorSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        list_serializer_class = SupervisorListSerializer


class PasswordResetSerializer(serializers.Serializer):
    """Custom serializer for Djoser's password reset view"""
    email = serializers.EmailField()
    organization = serializers.UUIDField()

    def get_user(self, is_active=True):
        try:
            user = models.User.objects.get(
                is_active=is_active,
                email=self.data.get('email', ''),
                organization=self.data.get('organization', ''),
            )
            if user.has_usable_password() and user.organization and user.organization.password_reset_url:
                return user
        except models.User.DoesNotExist:
            pass
