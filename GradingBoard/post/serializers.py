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


class CommentSerializer(serializers.ModelSerializer):
    """ Serializer for comments """

    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    post = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__' # ['id', 'user', 'post_id', 'text', 'created_at', 'modified_at']
        read_only = ['id', 'user', 'post', 'created_at', 'modified_at']

    def create(self, validated_data):
        """ Create a comment. """
        # user and post can not be assigned.
        validated_data.pop('user', None)
        # リクエストからpost_idを取得
        post_id = self.context['request'].parser_context['kwargs']['post_id']
        comment = Comment.objects.create(user=self.context['request'].user, post=post_id, **validated_data)

        return comment


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
        read_only = ['id', 'user', 'created_at', 'modified_at',]

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


    def get_comments(self):
        """ Retrieve comments """
        pass
