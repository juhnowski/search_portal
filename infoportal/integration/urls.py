from django.urls import path

from .views import *

urlpatterns = [
    path('import-journal', JournalApiView.as_view())
]
