"""
Views for the post APIs.
"""
# DRF -----
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
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


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet,):
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
                     # mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet,):
    serializer_class = serializers.CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id, comment_id):
        post_id = self.kwargs.get('post_id')
        comment_id = self.kwargs.get('comment_id')

        comment = get_object_or_404(Comment, post_id=post_id, id=comment_id)
        serializer = self.get_serializer(comment)
        return Response(serializer.data)


class DummySumView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id_one, id_two):
        try:
            # Assuming id_one and id_two are integers
            sum_result = int(id_one) + int(id_two)
            return Response({'sum': sum_result}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({'error': 'Invalid input. Please provide valid integers.'}, status=status.HTTP_400_BAD_REQUEST)
