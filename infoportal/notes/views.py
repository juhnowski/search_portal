from django.contrib.auth import get_user_model

from .models import Notes, Comments
from .serializers import *

from users.utils.permissions import *

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status


CustomUserModel = get_user_model()


class NotesListAPIView(generics.ListAPIView):
    """
    Возвращает список всех собственных заметок пользователя.
    """
    serializer_class = NotesSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Notes.objects.filter(owner=user)
        return queryset


class NotesCreateAPIView(generics.CreateAPIView):
    """
    Создание заметки.
    """
    serializer_class = NotesSerializer

    def create(self, request, *args, **kwargs):
        serializer = NotesSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OtherNotesListAPIView(generics.ListAPIView):
    """
    Возвращает список всех чужих заметок, к которым
    пользователю дан доступ.
    """
    serializer_class = NotesSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Notes.objects.filter(access_user=user)
        return queryset


class HandleNotesAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Работа с отдельной заметкой пользователя,
    заметку может просматривать только тот кто
    создал заметку или кому разрешен просмотр.
    Изменять, удалять заметку может только владелец.
    """
    def get_serializer_class(self):
        if self.request.method == 'GET':
            serializer_class = NotesSerializerWithAccess
        if self.request.method == 'PUT':
            serializer_class = NotesSerializer
        if self.request.method == 'PATCH':
            serializer_class = NotesSerializer
        if self.request.method == 'DELETE':
            serializer_class = NotesSerializer
        return serializer_class

    queryset = Notes.objects.all()
    permission_classes = (HandleOwnerOrAccessUserOnlyNotes|IsAdmin, )

    def update(self, request, *args, **kwargs):
        serializer = NotesSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = self.get_object()
            serializer.update(instance=instance, validated_data=request.data)
        return Response(request.data)

    def partial_update(self, request, *args, **kwargs):
        serializer = NotesSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            instance = self.get_object()
            serializer.update(instance=instance, validated_data=request.data)
        return Response(request.data)


class CommentsListAPIView(generics.ListAPIView):
    """
    Возвращает список всех комментариев к определенной заметке,
    владельцем заметки должен быть запрашивающий или тот, кому
    дано разрешение.
    """
    serializer_class = CommentSerializer
    permission_classes = (AccessUserOnlyComment|IsAdmin, )

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            queryset = Comments.objects.all()
            return Comments.objects.none()
        notes_id = self.kwargs['pk']
        queryset = Comments.objects.filter(notes__id=notes_id)
        return queryset


class CommentsCreateAPIView(generics.CreateAPIView):
    """
    Создает комментарий к определенной заметке. Комментарий
    может создавать только владелец заметки или тот, кому
    дано разрешение.
    """
    serializer_class = CommentCreateSerializer
    queryset = Comments.objects.all()
    permission_classes = (CreateOwnerOrAccessUserOnlyComment|IsAdmin, )

    def create(self, request, *args, **kwargs):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=self.request.user)
        notes_id = self.kwargs['pk']
        notes = Notes.objects.get(id=notes_id)
        comment = Comments.objects.get(id=serializer.data['id'])
        notes.comments.add(comment)
        return Response(serializer.data)


class HandleCommentsAPIView(generics.UpdateAPIView,
                            generics.DestroyAPIView):
    """
    Обновление, удаление комментария к заметке.
    Удалить, изменить комментарий может только владелец.
    """
    serializer_class = CommentCreateSerializer
    queryset = Comments.objects.all()
    permission_classes = (HandleOwnerOrAccessUserOnlyComment|IsAdmin, )

    def update(self, request, *args, **kwargs):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.update(instance=self.get_object(), validated_data=request.data)
        return Response(serializer.data)
        
