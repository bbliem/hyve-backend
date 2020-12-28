"""learning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from material import views

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'lessons', views.LessonViewSet)
router.register(r'organizations', views.OrganizationViewSet)
router.register(r'multiple-choice-answers', views.MultipleChoiceAnswerViewSet)
router.register(r'multiple-choice-questions', views.MultipleChoiceQuestionViewSet)
router.register(r'multiple-choice-responses', views.MultipleChoiceResponseViewSet)
router.register(r'open-questions', views.OpenQuestionViewSet)
router.register(r'open-question-responses', views.OpenQuestionResponseViewSet)
router.register(r'sections', views.SectionViewSet)
router.register(r'section-completions', views.SectionCompletionViewSet)
router.register(r'static-pages', views.StaticPageViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Security remark: obtain_auth_token has no throttling; cf.
    # https://www.django-rest-framework.org/api-guide/authentication/#generating-tokens
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.BROWSABLE_API:
    urlpatterns += [
        # Authentication endpoints for DRF's browsable API
        path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    ]
