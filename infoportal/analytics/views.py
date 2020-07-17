from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime, timedelta

from .serializers import *

from users.utils.permissions import *
from users.models import *
from documents.models import *


class AnalyticsAPIView(APIView):
    permission_classes = (IsRoleUR | IsRoleRD | IsRoleBL | IsRoleEX | IsAdmin,)
    serializer_class = AnalyticsSerializer

    def get(self, *args, **kwargs):
        serializer = self.serializer_class(Analytics.objects.last())
        return Response(serializer.data, status=status.HTTP_200_OK)


class DocumentsAnalyticsAPIView(APIView):
    permission_classes = (IsRoleUR | IsRoleRD | IsRoleBL | IsRoleEX | IsAdmin,)
    serializer_class = DocumentsAnalyticsSerializer

    def get(self, *args, **kwargs):
        serializer = self.serializer_class(Analytics.objects.last())
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersAnalyticsAPIView(APIView):
    permission_classes = (IsRoleUR | IsRoleRD | IsRoleBL | IsRoleEX | IsAdmin,)
    serializer_class = UsersAnalyticsSerializer

    def get(self, *args, **kwargs):
        serializer = self.serializer_class(Analytics.objects.last())
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompaniesAnalyticsAPIView(APIView):
    permission_classes = (IsRoleUR | IsRoleRD | IsRoleBL | IsRoleEX | IsAdmin,)
    serializer_class = CompaniesAnalyticsSerializer

    def get(self, *args, **kwargs):
        serializer = self.serializer_class(Analytics.objects.last())
        return Response(serializer.data, status=status.HTTP_200_OK)


class NotesAnalyticsAPIView(APIView):
    permission_classes = (IsRoleUR | IsRoleRD | IsRoleBL | IsRoleEX | IsAdmin,)
    serializer_class = NotesAnalyticsSerializer

    def get(self, *args, **kwargs):
        serializer = self.serializer_class(Analytics.objects.last())
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateNewAnalyticsRecordAPIView(generics.CreateAPIView):
    permission_classes = (IsAdmin, )
    serializer_class = CreateNewAnalyticsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        if serializer.create():
            return Response("Success", status=status.HTTP_201_CREATED)
        else:
            return Response("Fail", status=status.HTTP_403_FORBIDDEN)


class WeeklyAnalyticsAPIView(generics.GenericAPIView):
    permission_classes = (IsRoleUR | IsRoleRD | IsRoleBL | IsRoleEX | IsAdmin,)
    serializer_class = AnalyticsSerializer

    def get(self, *args, **kwargs):
        s_last = self.serializer_class(Analytics.objects.last())
        try:
            date = datetime.strptime(s_last.data['date'], "%Y-%m-%d").date() - timedelta(weeks=1)

            s_weekly = self.serializer_class(
                Analytics.objects.filter(date=date)[0]
            )

            docs_data = {}
            for field in s_weekly.data['documents']:
                if field != 'labels':
                    docs_data[field] = s_last.data['documents'][field] - s_weekly.data['documents'][field]
                else:
                    docs_data[field] = s_weekly.data['documents'][field]

            data = {
                'documents': docs_data,
                'users': s_last.data['users'] - s_weekly.data['users'],
                'companies': s_last.data['companies'] - s_weekly.data['companies'],
                'notes': s_last.data['notes'] - s_weekly.data['notes'],
                'labels': s_last.data['labels']
            }
            return Response(data, status=status.HTTP_200_OK)

        except IndexError:
            return Response(s_last.data, status=status.HTTP_200_OK)
