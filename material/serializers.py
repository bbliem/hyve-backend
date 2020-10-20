from rest_framework import serializers

from material import models


class SectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Section
        fields = ['text', 'questions']


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Question
        fields = ['text']


class LessonContentSerializer(serializers.HyperlinkedModelSerializer):
    text = serializers.ReadOnlyField(source='section.text')

    class Meta:
        model = models.LessonContent
        fields = ['id', 'text', 'page']


class LessonSerializer(serializers.HyperlinkedModelSerializer):
    sects = LessonContentSerializer(source='lessoncontent_set', many=True)
    # sections = serializers.HyperlinkedRelatedField(many=True, view_name='section-detail', read_only=True)

    class Meta:
        model = models.Lesson
        fields = ['name', 'description', 'sects']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Category
        fields = ['name', 'description', 'lessons']
