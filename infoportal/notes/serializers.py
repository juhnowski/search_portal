from django.contrib.auth import get_user_model

from rest_framework import serializers
from . import models

CustomUserModel = get_user_model()


class FullUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUserModel
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email')


class NotesSerializerWithAccess(serializers.ModelSerializer):
    access_user = FullUserSerializer(read_only=True, many=True)
    edit = serializers.SerializerMethodField('is_current_user_owner')

    class Meta:
        model = models.Notes
        exclude = ('comments', 'owner' )

    def is_current_user_owner(self, obj):
        current_user = self.context['request'].user
        if str(obj.owner.email) == str(current_user):
            return 'full'
        else:
            return 'none'


class NotesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Notes
        exclude = ('comments', 'owner' )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUserModel
        ref_name = 'user_comment'
        fields = ('first_name',
                  'last_name')


class CommentSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    edit = serializers.SerializerMethodField('is_current_user_owner')

    class Meta:
        model = models.Comments
        fields = ('id', 'owner', 'content', 'created', 'edit')

    def is_current_user_owner(self, obj):
        current_user = self.context['request'].user
        if str(obj.owner.email) == str(current_user):
            return 'full'
        else:
            return 'none'


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comments
        exclude = ('owner', )
