from django.shortcuts import render
from rest_framework import viewsets, permissions

from .models import Category, Lesson
from .serializers import CategorySerializer, LessonSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
