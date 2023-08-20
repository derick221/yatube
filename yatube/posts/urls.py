from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls import handler404, handler500
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('create_group/', views.create_group, name='create_group'),
    path('group/<slug:slug>/', views.group_posts, name='group_posts'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path("new/", views.PostView.as_view(), name="new_post"),
    path('about-author/', views.about_author, name='about_author'),
    path('about-technologies/', views.about_technologies, name='about_technologies'),
    path('<str:username>/<int:post_id>/', views.post_view, name='post_view'),
    path('<str:username>/<int:post_id>/detail/', views.post_detail, name='post_detail'),
    path('404/', TemplateView.as_view(template_name='misc/404.html'), name='custom_404'),
    path('500/', TemplateView.as_view(template_name='misc/500.html'), name='custom_500'),
    path("<username>/<int:post_id>/comment", views.add_comment, name="add_comment"),
    path('group/<slug:group_slug>/', views.group_view, name='group'),
    path("follow/", views.follow_index, name="follow_index"),
    path("<str:username>/follow/", views.profile_follow, name="profile_follow"), 
    path("<str:username>/unfollow/", views.profile_unfollow, name="profile_unfollow"),
    path("api-token-auth/", obtain_auth_token),
    path("api/v1/posts/", views.api_posts),
    path("api/v1/posts/<int:id>/", views.api_posts_detail),
]

handler404 = "posts.views.page_not_found"
handler500 = "posts.views.server_error"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
