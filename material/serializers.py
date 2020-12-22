from drf_base64.serializers import ModelSerializer as Base64ModelSerializer
from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers

from material import models


class StaticPageSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.StaticPage
        fields = ['url', 'id', 'title_en', 'title_fi', 'content_en', 'content_fi']


class MultipleChoiceAnswerSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.MultipleChoiceAnswer
        fields = ['url', 'id', 'question', 'text_en', 'text_fi', 'correct', 'explanation_en', 'explanation_fi']


class MultipleChoiceQuestionSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.MultipleChoiceQuestion
        fields = ['url', 'id', 'section', 'text_en', 'text_fi', 'answers']
        expandable_fields = {
            'answers': (MultipleChoiceAnswerSerializer, {'source': 'answers', 'many': True})
        }


class OpenQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OpenQuestion
        fields = ['url', 'id', 'section', 'text_en', 'text_fi']


class SectionSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Section
        fields = ['url', 'id', 'text_en', 'text_fi', 'multiple_choice_questions', 'open_questions']
        expandable_fields = {
            'multiple_choice_questions': (MultipleChoiceQuestionSerializer, {'source': 'multiple_choice_questions', 'many': True}),
            'open_questions': (OpenQuestionSerializer, {'source': 'open_questions', 'many': True}),
        }


class ContentSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Content
        fields = ['id', 'lesson', 'section', 'page']
        expandable_fields = {
            'section': (SectionSerializer, {'source': 'section'})
        }


class LessonSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = ['url', 'id', 'name_en', 'name_fi', 'description_en', 'description_fi', 'categories', 'sections']
        expandable_fields = {
            'contents': (ContentSerializer, {'source': 'content_set', 'many': True, 'omit': ['lesson']})
        }


class CategorySerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['url', 'id', 'name_en', 'name_fi', 'description_en', 'description_fi', 'lessons']
        expandable_fields = {
            'lessons': (LessonSerializer, {'many': True})
        }


class SectionCompletionSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.SectionCompletion
        fields = ['url', 'id', 'user', 'section', 'last_modified']

    def validate_user(self, value):
        if value != self.context['request'].user:
            raise serializers.ValidationError("User specified in SectionCompletion object is not yourself")
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
    Serializer for the Organization model meant for users that are not supervisors of the organization.

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


class OrganizationSerializerWithMembers(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    """
    Serializer for the Organization model meant for supervisors of the organization.
    """
    class Meta:
        model = models.Organization
        fields = ['url', 'id', 'name', 'lessons']

    expandable_fields = {
        'lessons': (LessonSerializer, {'source': 'lessons', 'many': True}),
        'users': (ContentSerializer, {'source': 'user_set', 'many': True, 'omit': ['organization']})
    }


class UserSerializer(FlexFieldsSerializerMixin, Base64ModelSerializer):
    class Meta:
        model = models.User
        fields = ['url', 'id', 'email', 'organization', 'username', 'name', 'avatar', 'is_supervisor', 'is_superuser', 'completed_sections']
        read_only_fields = ['organization', 'username', 'is_supervisor', 'is_superuser']
        expandable_fields = {
            'organization': OrganizationSerializer,
            'section_completions': (SectionCompletionSerializer, {'source': 'sectioncompletion_set', 'many': True, 'omit': ['user']}),
            'multiple_choice_responses': (MultipleChoiceResponseSerializer, {'source': 'multiplechoiceresponse_set', 'many': True, 'omit': ['user']}),
            'open_question_responses': (OpenQuestionResponseSerializer, {'source': 'openquestionresponse_set', 'many': True, 'omit': ['user']}),
        }
