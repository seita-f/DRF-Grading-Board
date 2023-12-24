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
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())
    faculty = serializers.PrimaryKeyRelatedField(queryset=Faculty.objects.all())
    class_name = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())
    professor = serializers.PrimaryKeyRelatedField(queryset=Professor.objects.all())

    class Meta:
        model = Post
        # all fields except description
        fields = ['id', 'school', 'faculty', 'class_name',
                  'professor', 'quality', 'difficulty', 'recommend',
                  'created_at', 'modified_at',]
        read_only = ['id', 'created_at', 'modified_at']


    def create(self, validated_data):
        """ Create a post. """
        post = Post.objects.create(**validated_data)
        return post

    def update(self, instance, validated_data):
        """ Update a post. """
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
