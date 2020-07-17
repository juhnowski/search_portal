from django.urls import path, include
from rest_framework import routers
from .views import *


urlpatterns = [
    path('', AnalyticsAPIView.as_view()),
    path('last/', AnalyticsAPIView.as_view()),
    path('documents/', DocumentsAnalyticsAPIView.as_view()),
    path('users/', UsersAnalyticsAPIView.as_view()),
    path('companies/', CompaniesAnalyticsAPIView.as_view()),
    path('notes/', NotesAnalyticsAPIView.as_view()),
    path('create/', CreateNewAnalyticsRecordAPIView.as_view()),
    path('last_week/', WeeklyAnalyticsAPIView.as_view()),
]
