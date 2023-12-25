"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter
from post import views

router = DefaultRouter()
router.register('', views.PostViewSet, basename='post')
router.register(r'(?P<id>\d+)/comment', views.CommentViewSet, basename='comment')

app_name = 'post'

urlpatterns = [
    path('', include(router.urls)),
]
