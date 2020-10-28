from django.conf import settings
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.settings import api_settings

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


# Disabled for now. Maybe we'll need it later...
# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = models.User.objects.all()
#     serializer_class = serializers.UserSerializer
#
#     def get_permissions(self):
#         if self.action == 'list':
#             self.permission_classes = [permissions.IsSuperUser]
#         else:
#             self.permission_classes = [permissions.IsOwnAccount]
#         return super().get_permissions()


class AuthTokenWithUserData(ObtainAuthToken):
    # Without setting this explicitly, DRF will just use JSONRenderer and ignore the camel-case renderer that we set.
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        serialized_user = serializers.UserSerializer(user, context={'request': request})
        return Response({
            'token': token.key,
            'user': serialized_user.data,
        })