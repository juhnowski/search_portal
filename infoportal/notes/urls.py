from django.urls import path

from .views import *


urlpatterns = [
    path('', NotesListAPIView.as_view()),
    path('create', NotesCreateAPIView.as_view()),
    path('other', OtherNotesListAPIView.as_view()),
    path('<int:pk>', HandleNotesAPIView.as_view()),

    path('<int:pk>/comments', CommentsListAPIView.as_view()),
    path('<int:pk>/commentcreate', CommentsCreateAPIView.as_view()),
    path('comments/<int:pk>', HandleCommentsAPIView.as_view()),
]