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
router.register('', views.PostViewSet, basename='post') # Post
router.register(r'(?P<id>\d+)/comment', views.CommentViewSet, basename='comment') # comments (GET List, CREATE Comment)

app_name = 'post'

urlpatterns = [
    path('', include(router.urls)),

    # comment detail GET/PATCH/DELETE
    path('<int:post_id>/comment/<int:comment_id>/', views.CommentDetailViewSet.as_view({'get': 'get'}), name='comment-detail'),
]
