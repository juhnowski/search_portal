from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Folders
from documents.models import Documents
from notes.models import Notes

CustomUserModel = get_user_model()


class RecursiveField(serializers.Serializer):
    """
    рекурсивное поле для сериализации mptt
    """
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class FolderSerializer(serializers.ModelSerializer):
    """
    сериализация дерева папок
    """
    subfolders = RecursiveField(source='parent_folder', many=True,
                                required=False, read_only=True)

    class Meta:
        model = Folders
        fields = ('id', 'name', 'subfolders')


class DocumentsSerializer(serializers.ModelSerializer):
    """
    получить название вложенного в папку документа
    """

    class Meta:
        model = Documents
        fields = ('id', 'doc_name_ru')
        ref_name = 'docs'


class NotesSerializer(serializers.ModelSerializer):
    """
    получить название вложенной в папку зметки
    """

    class Meta:
        model = Notes
        fields = ('id', 'name')
        ref_name = 'nots'


class CustomUserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUserModel
        fields = ('id', 'first_name', 'last_name', 'email')


class RetrieveFolderSerializer(serializers.ModelSerializer):
    """
    сериализация отдельной папки, метод GET с получением
    имен вложенных документов, заметок и пользователей,
    кому расшарена папка
    """
    documents = DocumentsSerializer(many=True, read_only=True)
    notes = NotesSerializer(many=True, read_only=True)
    subfolders = RecursiveField(source='parent_folder', many=True,
                                required=False, read_only=True)
    access_user = CustomUserModelSerializer(many=True, read_only=True)

    class Meta:
        model = Folders
        fields = ('id',
                  'name',
                  'access_user',
                  'documents',
                  'notes',
                  'subfolders')


class UpdateFolderSerializer(serializers.ModelSerializer):
    """
    сериализация отдельной папки, методы PUT, PATH, DELETE
    """
    subfolders = RecursiveField(source='parent_folder', many=True,
                                required=False, read_only=True)

    class Meta:
        model = Folders
        fields = ('id',
                  'name',
                  'access_user',
                  'documents',
                  'notes',
                  'subfolders')


class FolderCreateSerializer(serializers.Serializer):
    """
    сериализация метода create для отдельной папки
    """
    id = serializers.IntegerField(help_text='id папки, в которой создается контент') # noqa
    type_content = serializers.CharField(
               max_length=30,
               write_only=True,
               help_text='тип добавляемого контента folders/documents/notes')
    id_content = serializers.IntegerField(help_text='id добавляемого контента',
                                          required=False,
                                          write_only=True)
    parent = serializers.CharField(max_length=50,
                                   required=False,
                                   help_text='название вновь создаваемой папки') # noqa

    def create(self, validated_data):
        user = self.context['request'].user
        id = validated_data.pop('id')
        type_content = validated_data.pop('type_content')
        id_content = validated_data.pop('id_content', None)
        parent = validated_data.pop('parent', None)
        
        folder = get_object_or_404(Folders, id=id)
        if type_content == 'folders':
            folder_new = Folders(name=parent, owner=user)
            folder_new.insert_at(folder, position='last-child', save=True)
        elif type_content == 'documents':
            folder.documents.add(Documents.objects.get(id=id_content))
        elif type_content == 'notes':
            folder.notes.add(Notes.objects.get(id=id_content))
        return folder
