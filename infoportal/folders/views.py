from django.contrib.auth import get_user_model

from rest_framework import generics

from .serializers import FolderSerializer, FolderCreateSerializer, \
    RetrieveFolderSerializer, UpdateFolderSerializer
from .models import Folders

from users.utils.permissions import *

CustomUserModel = get_user_model()


class FolderShemaAPIView(generics.ListAPIView):
    """
    Возвращает дерево папок для определенного
    пользователя
    """
    serializer_class = FolderSerializer
    pagination_class = None

    def get_queryset(self):
        email_user = self.request.user
        user = CustomUserModel.objects.get(email=email_user)
        return Folders.objects.root_nodes().filter(owner_id=user.id)


class FolderShareAPIView(generics.ListAPIView):
    """
    Возвращает расшареные папки для определенного
    пользователя
    """
    serializer_class = FolderSerializer
    pagination_class = None

    def get_queryset(self):
        # делаем, чтобы дубликаты расшареных папок не попали в список
        # если у расшареной папки родитель тоже расшареный
        email_user = self.request.user
        user = CustomUserModel.objects.get(email=email_user)
        nodes = Folders.objects.filter(access_user=user.id)
        dublicate_nodes = []
        for node in nodes:
            children = node.get_children()
            list_children = []
            for child in children:
                list_children.append(child.id)
            for node_two in nodes:
                if node_two.id in list_children:
                    dublicate_nodes.append(node_two.id)
        return Folders.objects.filter(access_user=user.id).exclude(id__in=dublicate_nodes) # NoQa


class FolderCreateAPIView(generics.CreateAPIView):
    """
    добавление контента в дерево
    """
    serializer_class = FolderCreateSerializer
    permission_classes = (FoldersOwnerOnly|IsAdmin, )


class FolderRetrieveAPIView(generics.RetrieveAPIView):
    """
    получить отдельную папку в дереве
    """
    queryset = Folders.objects.all() 
    serializer_class = RetrieveFolderSerializer
    permission_classes = (HandleOwnerOrAccessUserOnlyFolder|IsAdmin, )


class FolderUpdateAPIView(generics.UpdateAPIView,
                          generics.DestroyAPIView):
    """
    изменение, удаление отдельной папки в дереве
    """
    queryset = Folders.objects.all() 
    serializer_class = UpdateFolderSerializer
    permission_classes = (HandleOwnerOrAccessUserOnlyFolder|IsAdmin, )

