from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.settings import api_settings

from material import models
from material import permissions
from material import serializers


class StaticPageViewSet(viewsets.ModelViewSet):
    queryset = models.StaticPage.objects.all()
    serializer_class = serializers.StaticPageSerializer
    permission_classes = [permissions.IsSuperUserOrReadOnly]


class SectionViewSet(viewsets.ModelViewSet):
    queryset = models.Section.objects.all()
    serializer_class = serializers.SectionSerializer
    permission_classes = [permissions.IsSuperUserOrReadOnly]


class MultipleChoiceQuestionViewSet(viewsets.ModelViewSet):
    queryset = models.MultipleChoiceQuestion.objects.all()
    serializer_class = serializers.MultipleChoiceQuestionSerializer
    permission_classes = [permissions.IsSuperUserOrReadOnly]


class MultipleChoiceAnswerViewSet(viewsets.ModelViewSet):
    queryset = models.MultipleChoiceAnswer.objects.all()
    serializer_class = serializers.MultipleChoiceAnswerSerializer
    permission_classes = [permissions.IsSuperUserOrReadOnly]


class OpenQuestionViewSet(viewsets.ModelViewSet):
    queryset = models.OpenQuestion.objects.all()
    serializer_class = serializers.OpenQuestionSerializer
    permission_classes = [permissions.IsSuperUserOrReadOnly]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = models.Lesson.objects.all()
    serializer_class = serializers.LessonSerializer
    permission_classes = [permissions.IsSuperUserOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsSuperUserOrReadOnly]


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    View for getting and updating user info.

    Creation/deletion should be done with the Djoser views. Also required fields (email, password) should be changed
    there.
    """
    # TODO make sure we can't change required fields in this view
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [permissions.IsSuperUser]
        else:
            self.permission_classes = [permissions.IsOwnAccount]
        return super().get_permissions()


class SectionCompletionViewSet(mixins.CreateModelMixin,
                               mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    queryset = models.SectionCompletion.objects.all()
    serializer_class = serializers.SectionCompletionSerializer
    permission_classes = [permissions.IsOwner]


class MultipleChoiceResponseViewSet(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    queryset = models.MultipleChoiceResponse.objects.all()
    serializer_class = serializers.MultipleChoiceResponseSerializer
    permission_classes = [permissions.IsOwner]


class OpenQuestionResponseViewSet(mixins.CreateModelMixin,
                                  mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.DestroyModelMixin,
                                  viewsets.GenericViewSet):
    queryset = models.OpenQuestionResponse.objects.all()
    serializer_class = serializers.OpenQuestionResponseSerializer
    permission_classes = [permissions.IsOwner]


class OrganizationViewSet(mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    queryset = models.Organization.objects.all()
    # permission_classes = [permissions.IsSupervisorOfThisOrganizationOrReadOnly]

    def get_serializer_class(self):
        """
        Return serializer that includes membership data iff retrieving a specific organization of which the
        requesting user is a supervisor.
        """
        if (self.action == 'retrieve'
                and self.request.user.is_authenticated
                and self.request.user.organization == self.get_object()
                and self.request.user.is_supervisor):
            return serializers.OrganizationSerializerWithMembers
        return serializers.OrganizationSerializer
