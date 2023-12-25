"""
Views for the post APIs.
"""
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Post,
    Comment,
)
from post import serializers


class PostViewSet(viewsets.ModelViewSet):
    """ View for managing post APIs. """
    serializer_class = serializers.PostDetailSerializer
    queryset = Post.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Retrieve all post (newest order) """
        return self.queryset.order_by('-created_at')

    def get_serializer_class(self):
        """ Return the serializer class for request """
        # except description (api/post/)
        if self.action == 'list':
            return serializers.PostSerializer

        # with description (api/post/{id})
        return self.serializer_class

    def perform_create(self, serializer):
        """ Create a new post """
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id).order_by('-created_at')

    def perform_create(self, serializer):
        """ Create a new comment """
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(user=self.request.user, post=post)
