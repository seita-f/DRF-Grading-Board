"""
Views for the post APIs.
"""
# DRF -----
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import views
from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Local -----
from core.models import (
    Post,
    Comment,
)
from .filters import (
    PostFilter,
)
from post import serializers


class PostViewSet(viewsets.ModelViewSet):
    """ View for managing post APIs. """
    serializer_class = serializers.PostDetailSerializer
    queryset = Post.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # filter
    filterset_class = PostFilter

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

    def destroy(self, request, *args, **kwargs):
        """ Delete a post """
        try:
            instance = self.get_object()

            # Check if the requesting user is the creator of the post
            if instance.user == request.user:
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied("You do not have permission to delete this post.")

        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet,):
    """ View for managing comment APIs. """
    serializer_class = serializers.CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Get comments in a post  """
        post_id = self.kwargs.get('id')
        return Comment.objects.filter(post_id=post_id).order_by('-created_at')

    def perform_create(self, serializer):
        """ Create a new comment """
        post_id = self.kwargs.get('id')

        post = get_object_or_404(Post, id=post_id)
        # post = Post.objects.get(id=post_id)
        serializer.save(user=self.request.user, post=post)


class CommentDetailViewSet(# mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet,):
    """ View for managing comment detail APIs. """
    serializer_class = serializers.CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def get(self, request, id, comment_id):
        """ Get a certaiin comment in a post """
        post_id = self.kwargs.get('id')
        comment_id = self.kwargs.get('comment_id')

        comment = get_object_or_404(Comment, post_id=post_id, id=comment_id)
        serializer = self.get_serializer(comment)
        return Response(serializer.data)

    # I do not implemnt PATCH (partial_update) since there is only one filed to fix -> text
    @action(detail=True, methods=['put'])
    def update(self, request, id, comment_id):
        """ Update a certain comment """
        post_id = self.kwargs.get('id')
        comment_id = self.kwargs.get('comment_id')

        comment = get_object_or_404(Comment, post_id=post_id, id=comment_id)
        serializer = self.get_serializer(comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def delete(self, request, *args, **kwargs):
        """ Delete a certain comment """
        post_id = self.kwargs.get('id')
        comment_id = self.kwargs.get('comment_id')

        comment = get_object_or_404(Comment, post_id=post_id, id=comment_id)

        # Compare the comment owner with the authenticated user
        if comment.user != request.user:
            return Response({"detail": "You don't have permission to delete this comment."},
                            status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response(status=204)
