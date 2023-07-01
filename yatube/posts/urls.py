from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('create_group/', views.create_group, name='create_group'),
    path('group/<slug:slug>/', views.group_posts, name='group_posts'),
    path('registration/', views.register, name='registration'),
]