from django.urls import path, include
from .views import MemberListAPI, MemberAPI

urlpatterns = [
    #path("hello", hello_api),
    path('members/', MemberListAPI.as_view()),
    path('members/<str:uid>', MemberAPI.as_view())
]