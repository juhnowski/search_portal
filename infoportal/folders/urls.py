from django.urls import path

from .views import *


urlpatterns = [
    path('shema', FolderShemaAPIView.as_view()),
    path('create', FolderCreateAPIView.as_view()),
    path('share', FolderShareAPIView.as_view()),
    path('<int:pk>/retrive', FolderRetrieveAPIView.as_view()),
    path('<int:pk>', FolderUpdateAPIView.as_view()),
]
