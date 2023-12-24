"""
Serializes for recipe APIs
"""
from rest_framework import serializers

from core.models import (
    User,
    School,
    Faculty,
    Class,
    Professor,
    Post,
    Comment,
)


class PostSerializer(serializers.ModelSerializer):
    """ Serializer for posts. """

    # Use serializers for related fields to make them selectable
    school_id = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())
    faculty_id = serializers.PrimaryKeyRelatedField(queryset=Faculty.objects.all())
    class_id = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())
    professor_id = serializers.PrimaryKeyRelatedField(queryset=Professor.objects.all())

    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        # all fields except description
        fields = ['id', 'user', 'school_id', 'faculty_id', 'class_id',
                  'professor_id', 'quality', 'difficulty', 'recommend',
                  'created_at', 'modified_at',]
        read_only = ['id', 'user', 'created_at', 'modified_at']

    def create(self, validated_data):
        """ Create a post. """
        # user can not be assigned.
        post = Post.objects.create(user=self.context['request'].user, **validated_data)
        return post

    def update(self, instance, validated_data):
        """ Update a post. """
        # Ensure that the 'user' field is read-only during updates
        validated_data.pop('user', None)

        # Only authenticated user can edit
        auth_user = self.context['request'].user
        
        if instance.user != auth_user:
            raise serializers.ValidationError("You do not have permission to edit this post.")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class PostDetailSerializer(PostSerializer):
    """ Serializer for a post detail view """
    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ['description']
