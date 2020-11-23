from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers

from material import models


class StaticPageSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.StaticPage
        fields = ['url', 'id', 'title_en', 'title_fi', 'content_en', 'content_fi']


class AnswerSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ['url', 'id', 'question', 'text_en', 'text_fi', 'correct']


class QuestionSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ['url', 'id', 'section', 'text_en', 'text_fi', 'answers']
        expandable_fields = {
            'answers': (AnswerSerializer, {'source': 'answers', 'many': True, 'omit': ['question']})
        }


class SectionSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Section
        fields = ['url', 'id', 'text_en', 'text_fi', 'questions']
        expandable_fields = {
            'questions': (QuestionSerializer, {'source': 'questions', 'many': True})
        }


class ContentSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Content
        fields = ['lesson', 'section', 'page']
        expandable_fields = {
            'section': (SectionSerializer, {'source': 'section'})
        }


class LessonSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    contents = ContentSerializer(source='content_set', many=True, omit=['lesson'])

    class Meta:
        model = models.Lesson
        fields = ['url', 'id', 'name_en', 'name_fi', 'description_en', 'description_fi', 'contents']
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


class UserSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['url', 'id', 'email', 'name', 'is_superuser', 'completed_sections']
        read_only_fields = ['is_superuser']
        expandable_fields = {
            'section_completions': (SectionCompletionSerializer, {'source': 'sectioncompletion_set', 'many': True, 'omit': ['user']})
        }
