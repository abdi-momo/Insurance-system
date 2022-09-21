from django.contrib import admin
from django.urls import path
from . import views
from .views import AccountListView


app_name = "account"

urlpatterns = [
    path('user/add_user/', views.add_user_view, name='add_user'),
    path('register/',views.register,name = "register"),
    path('login/',views.loginUser,name = "login"),
    path('logout/',views.logoutUser,name = "logout"),
    path('userListe/',views.userList,name = "userListe"),
    path('accounts/', AccountListView.as_view(), name='all_accounts'),
]
