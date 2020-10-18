from django.shortcuts import render
from rest_framework import viewsets, permissions

from .models import Category, Content
from .serializers import CategorySerializer, ContentSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ContentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
