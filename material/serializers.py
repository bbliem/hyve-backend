from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers

from material import models


class AnswerSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ['id', 'question', 'text', 'correct']


class QuestionSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ['id', 'section', 'text', 'answers']
        expandable_fields = {
            'answers': (AnswerSerializer, {'source': 'answers', 'many': True, 'omit': ['question']})
        }


class SectionSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Section
        fields = ['id', 'text', 'questions']
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
        fields = ['id', 'name', 'description', 'contents']
        expandable_fields = {
            'contents': (ContentSerializer, {'source': 'content_set', 'many': True, 'omit': ['lesson']})
        }


class CategorySerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'name', 'description', 'lessons']
        expandable_fields = {
            'lessons': (LessonSerializer, {'many': True})
        }
