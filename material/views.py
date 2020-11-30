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


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = [permissions.IsSuperUserOrReadOnly]


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    permission_classes = [permissions.IsSuperUserOrReadOnly]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = models.Lesson.objects.all()
    serializer_class = serializers.LessonSerializer
    permission_classes = [permissions.IsSuperUserOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsSuperUserOrReadOnly]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [permissions.IsSuperUser]
        else:
            self.permission_classes = [permissions.IsOwnAccount]
        return super().get_permissions()


class AuthTokenWithUserData(ObtainAuthToken):
    # Without setting this explicitly, DRF will just use JSONRenderer and ignore the camel-case renderer that we set.
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        serialized_user = serializers.UserSerializer(user,
                                                     context={'request': request},
                                                     omit=['completed_sections'],
                                                     expand=['section_completions'])
        return Response({
            'token': token.key,
            'user': serialized_user.data,
        })


class SectionCompletionViewSet(mixins.CreateModelMixin,
                               mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    queryset = models.SectionCompletion.objects.all()
    serializer_class = serializers.SectionCompletionSerializer
    permission_classes = [permissions.IsOwner]


class QuestionResponseViewSet(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    queryset = models.QuestionResponse.objects.all()
    serializer_class = serializers.QuestionResponseSerializer
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
        if self.action == 'retrieve' and self.request.user.is_authenticated:
            try:
                membership = self.request.user.membership_set.get(organization=self.get_object())
                if membership.is_supervisor:
                    return serializers.OrganizationSerializerWithMembers
            except models.Membership.DoesNotExist:
                pass
        return serializers.OrganizationSerializer
