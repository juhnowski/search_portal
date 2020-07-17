from django.urls import path

from .views import *


urlpatterns = [
    path('', CompareHTML.as_view()),
]
