from rest_framework import viewsets

from material import models
from material import permissions
from material import serializers


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


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [permissions.IsSuperUser]
        else:
            self.permission_classes = [permissions.IsOwnAccount]
        return super().get_permissions()
