from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from material import models
from material import serializers
from material import permissions


class SectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Section.objects.all()
    serializer_class = serializers.SectionSerializer


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer


class AnswerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Lesson.objects.all()
    serializer_class = serializers.LessonSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsOwnAccountOrReadOnly]
