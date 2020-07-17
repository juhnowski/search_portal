from django.urls import path

from .views import UserListAPIView, UserRetrieveAPIView, login, \
    UserCreateAPIView, check_token, UserSearchAPIView, \
    UserAdvancedSearchAPIView


urlpatterns = [
    path('v1/login', login),

    path('v1/users', UserListAPIView.as_view()),
    path('v1/users/<int:pk>', UserRetrieveAPIView.as_view()),
    path('v1/users/create', UserCreateAPIView.as_view()),

    path('v1/users/search/', UserSearchAPIView.as_view()),
    path('v1/users/advanced_search/', UserAdvancedSearchAPIView.as_view()),

    path('v1/check_token/', check_token),

]
