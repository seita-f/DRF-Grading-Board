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

#------------------------------------------------------------------------------------------

class PostSerializer(serializers.ModelSerializer):
    """ Serializer for posts. """

    # Use serializers for related fields to make them selectable
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())
    faculty = serializers.PrimaryKeyRelatedField(queryset=Faculty.objects.all())
    _class = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())
    professor = serializers.PrimaryKeyRelatedField(queryset=Professor.objects.all())

    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    # comments = PostCommentSerializer(source='comments.text')

    class Meta:
        model = Post
        # all fields except description
        fields = ['id', 'user', 'school', 'faculty', '_class',
                  'professor', 'quality', 'difficulty', 'recommend',
                  'created_at', 'modified_at',]
        read_only = ['id', 'post_id', 'user', 'created_at', 'modified_at',]

    def create(self, validated_data):
        """ Create a post. """
        # user can not be assigned.
        validated_data.pop('user', None)
        post = Post.objects.create(user=self.context['request'].user, **validated_data)
        return post

    def update(self, instance, validated_data):
        """ Update a post. """
        # Ensure that the 'user' field is read-only during updates
        validated_data.pop('user', None)

        # Only authenticated user can edit
        auth_user = self.context['request'].user

        if instance.user != auth_user:
            raise serializers.ValidationError('You do not have permission to edit this post.')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class PostDetailSerializer(PostSerializer):
    """ Serializer for a post detail view """
    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ['description']
