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
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from material import views

router = routers.DefaultRouter()
router.register(r'answers', views.AnswerViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'lessons', views.LessonViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'sections', views.SectionViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Security remark: obtain_auth_token has no throttling; cf.
    # https://www.django-rest-framework.org/api-guide/authentication/#generating-tokens
    path('api-token-auth/', obtain_auth_token),
    path('admin/', admin.site.urls),
]
