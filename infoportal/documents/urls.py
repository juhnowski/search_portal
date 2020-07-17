from django.urls import path

from .views import *


urlpatterns = [
    path('', DocumentsListAPIView.as_view()),
    path('<int:pk>', ShortDocumentAPIView.as_view()),
    path('<int:pk>/bibliography', DocumentAPIView.as_view()),
    path('<int:id>/content', content),
    path('<int:pk>/rate', RateDocumentAPIView.as_view()),

    path('<int:pk>/notice', NoticeDocumentAPIView.as_view()),
    path('<int:pk>/noticecreate', NoticeCreateDocumentAPIView.as_view()),
    path('textsettings/<int:pk>', TextSettingsAPIView.as_view()),
    path('comments/<int:pk>', CommentsAPIView.as_view()),
    path('textsettings/<int:pk>/create', CreateTextSettingsAPIView.as_view()),
    path('comments/<int:pk>/create', CreateCommentsAPIView.as_view()),

    path('form', documents, name='form-upload'),
]
