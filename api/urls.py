from api.views import *
from django.urls import path

urlpatterns = [
    path("login", LoginAPIView.as_view()),
    path("register", RegisterAPIView.as_view()),
    path("getUser/<str:query>", UserSearchView.as_view(),name='user-search'),
    path("editUser/<str:pk>", EditUserProfile.as_view()),    
    path("users/me", UserDetail.as_view())
]