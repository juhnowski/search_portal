from django.shortcuts import get_object_or_404

from rest_framework import permissions

from notes.models import Notes
from folders.models import Folders
from documents.models import DocumentsNotice

class IsAdmin(permissions.BasePermission):
    """
    Разрешения для администратора
    """
    def has_permission(self, request, view):
        return request.user.is_superuser
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class IsStaff(permissions.BasePermission):
    """
    Разрешения для пользователя с ролью is_staff
    """

    def has_permission(self, request, view):
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff


class IsRoleGA(permissions.BasePermission):
    """
    Разрешения для пользователя с ролью Админ группы
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'GA':
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'GA':
            return True
        else:
            return False


class IsRoleBL(permissions.BasePermission):
    """
    Разрешения для пользователя с ролью Библиотека
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'BL':
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'BL':
            return True
        else:
            return False


class IsRoleRD(permissions.BasePermission):
    """
    Разрешения для пользователя с ролью Читатель
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'RD':
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'RD':
            return True
        else:
            return False


class IsRoleUR(permissions.BasePermission):
    """
    Разрешения для пользователя с ролью Пользователь
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False 
        if request.user.role == 'UR':
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'UR':
            return True
        else:
            return False


class IsRoleEX(permissions.BasePermission):
    """
    Разрешения для пользователя с ролью Эксперт
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'EX':
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'EX':
            return True
        else:
            return False


class GetAndUpdateOwnerOnly(permissions.BasePermission):
    """
    Разрешение:
        - позволяет делать GET, PUT и PATCH в свои "собственные" записи
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.method == 'GET':
            if obj.id == request.user.id:
                return True
            else:
                return False

        if request.method == 'PUT':
            if obj.id == request.user.id:
                return True
            else:
                return False

        if request.method == 'PATCH':
            if obj.id == request.user.id:
                return True
            else:
                return False


class HandleOwnerOrAccessUserOnlyNotes(permissions.BasePermission):
    """
    Разрешение для заметки пользователя:
        - позволяет делать GET в свои "собственные" заметки или кому разрешено
        - PUT, PATCH, DELETE только для "владельца" заметки
    """

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            if not request.user.is_authenticated:
                return False
            notes = Notes.objects.get(id=obj.id)
            access_user = notes.access_user.all()
            users = []
            for user in access_user:
                users.append(user.id)
            # проверяем является ли текущий юзер владельцем заметки
            # или заметка ему расшарена
            if str(obj.owner) == str(request.user.email) or request.user.id in users:
                return True
            # проверяем находится ли данная заметка в расшареной папке
            if Folders.objects.filter(notes__id=obj.id).filter(access_user=request.user.id).exists(): # NoQa
                return True
            # если данная заметка находится в любой папке
            if Folders.objects.filter(notes__id=obj.id).exists():
                folders = Folders.objects.filter(notes__id=obj.id)
                list_ancestors_access_user = []
                # проверяем не расшарена ли папка выше по дереву
                for folder in folders:
                    folders_ancestors = folder.get_ancestors()
                    for i in folders_ancestors:
                        for j in i.access_user.all():
                            list_ancestors_access_user.append(j.email)
                if request.user.email in set(list_ancestors_access_user):
                    return True
            return False

        if request.method == 'PUT':
            if request.user.is_authenticated and str(obj.owner) == str(request.user.email):
                return True
            else:
                return False

        if request.method == 'PATCH':
            if request.user.is_authenticated and str(obj.owner) == str(request.user.email):
                return True
            else:
                return False

        if request.method == 'DELETE':
            if request.user.is_authenticated and str(obj.owner) == str(request.user.email):
                return True
            else:
                return False


class CreateOwnerOrAccessUserOnlyComment(permissions.BasePermission):
    """
    Разрешение для комментария к заметке:
        - позволяет делать POST в свои "собственные" записи или кому разрешено
    """

    def has_permission(self, request, view):
        notes_id = request.resolver_match.kwargs.get('pk')
        notes = Notes.objects.get(id=notes_id)
        access_user = notes.access_user.all()
        users = []
        for user in access_user:
            users.append(user.id)
        # если коммент принадлежит заметке, владельцем которой
        # является текущий юзер или заметка ему расшарена
        if str(notes.owner) == str(request.user) or request.user.id in users: # NoQa
            return True
        # проверяем находится ли коммент в расшареной папке
        if Folders.objects.filter(notes__id=notes_id).filter(access_user=request.user.id).exists(): # NoQa
            return True
        # если коммент находится в любой папке
        if Folders.objects.filter(notes__id=notes_id).exists():
            folders = Folders.objects.filter(notes__id=notes_id)
            list_ancestors_access_user = []
            # проверяем не расшарена ли папка выше по дереву
            for folder in folders:
                folders_ancestors = folder.get_ancestors()
                for i in folders_ancestors:
                    for j in i.access_user.all():
                        list_ancestors_access_user.append(j.email)
            if request.user.email in set(list_ancestors_access_user):
                return True
        return False


class AccessUserOnlyComment(permissions.BasePermission):
    """
    Разрешение для комментария к заметке:
        - позволяет делать GET свои "собственные" записи или кому разрешено
    """
    def has_permission(self, request, view):
        notes_id = request.resolver_match.kwargs.get('pk')
        notes = get_object_or_404(Notes, id=notes_id)
        access_user = notes.access_user.all()
        users = []
        for user in access_user:
            users.append(user.id)
        # если коммент принадлежит заметке, владельцем которой
        # является текущий юзер или заметка ему расшарена
        if str(notes.owner) == str(request.user) or request.user.id in users: # NoQa
            return True
        # проверяем находится ли коммент в расшареной папке
        if Folders.objects.filter(notes__id=notes_id).filter(access_user=request.user.id).exists(): # NoQa
            return True
        # если коммент находится в любой папке
        if Folders.objects.filter(notes__id=notes_id).exists():
            folders = Folders.objects.filter(notes__id=notes_id)
            list_ancestors_access_user = []
            # проверяем не расшарена ли папка выше по дереву
            for folder in folders:
                folders_ancestors = folder.get_ancestors()
                for i in folders_ancestors:
                    for j in i.access_user.all():
                        list_ancestors_access_user.append(j.email)
            if request.user.email in set(list_ancestors_access_user):
                return True
        return False


class HandleOwnerOrAccessUserOnlyComment(permissions.BasePermission):
    """
    Разрешение для комментария в заметке пользователя:
        - PUT, PATCH, DELETE только для "владельца" записи
    """

    def has_object_permission(self, request, view, obj):
        if str(obj.owner) == str(request.user.email):
            return True
        else:
            return False


class FoldersOwnerOnly(permissions.BasePermission):
    """
    Разрешение для создания папки пользователя в Избранном:
        - позволяет создавать папку только в своем дереве
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            try:
                folder_id = request.data['id']
            except KeyError:
                return True
            user_id = request.user.id
            folder = get_object_or_404(Folders, id=folder_id)
            owner = folder.owner.id
            if owner == user_id:
                return True
            else:
                return False


class HandleOwnerOrAccessUserOnlyFolder(permissions.BasePermission):
    """
    Разрешение для папки пользователя:
        - позволяет делать GET в свои "собственные" папки или кому разрешено
        - PUT, PATCH, DELETE только для "владельца" папки
    """

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            if not request.user.is_authenticated:
                return False
            list_access_user = []
            for i in obj.access_user.all():
                list_access_user.append(i.email)
            # проверяем является ли текущий юзер владельцем папки
            # или ему расшарена данная папка
            if str(obj.owner) == request.user.email or request.user.email in list_access_user: # NoQa
                return True
            # проверяем является ли текущий юзер владельцем папки выше по дереву
            # или ему расшарена папка выше по дереву
            else:
                folders_ancestors = obj.get_ancestors()
                list_ancestors_access_user = []
                for folder in folders_ancestors:
                    for i in folder.access_user.all():
                        list_ancestors_access_user.append(i.email)
                    list_ancestors_access_user.append(folder.owner.email)
                if request.user.email in set(list_ancestors_access_user):
                    return True
            return False

        if request.method == 'PUT':
            if request.user.is_authenticated and str(obj.owner) == request.user.email:
                return True
            else:
                return False

        if request.method == 'PATCH':
            if request.user.is_authenticated and str(obj.owner) == request.user.email:
                return True
            else:
                return False

        if request.method == 'DELETE':
            if request.user.is_authenticated and str(obj.owner) == request.user.email:
                return True
            else:
                return False


class HandleOwnerOnlyDocumentsNotice(permissions.BasePermission):
    """
    Разрешение для закладок в документе:
        - PUT, PATCH, DELETE только для "владельца" закладки
    """

    def has_object_permission(self, request, view, obj):

        if not request.user.is_authenticated:
            return False

        if DocumentsNotice.objects.filter(text_settings=obj.id). \
                               filter(user=request.user.id).exists():
            return True
        elif DocumentsNotice.objects.filter(comments=obj.id). \
                               filter(user=request.user.id).exists():
            return True
        else:
            return False
