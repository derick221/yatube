from django.contrib import admin
from django.urls import include, path
from django.contrib.flatpages import views as flatpages_views
from posts import views as posts_views
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("posts.urls")),
    path('<str:username>/', posts_views.profile, name='profile'),
    path('<str:username>/<int:post_id>/', posts_views.post_view, name='post'),
    path('<str:username>/<int:post_id>/edit/', posts_views.post_edit, name='post_edit'),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path('about/', include('django.contrib.flatpages.urls')),
    path('about-author/', posts_views.about_author, name='about_author'),
    path('about-spec/', posts_views.about_technologies, name='about_technologies'),
    path('about-us/', flatpages_views.flatpage, {'url': '/about-us/'}, name='about_us'),
    path('terms/', flatpages_views.flatpage, {'url': '/terms/'}, name='terms'),
    path('rasskaz-o-tom-kakie-my-horoshie/', flatpages_views.flatpage, {'url': '/rasskaz-o-tom-kakie-my-horoshie/'}, name='rasskaz_o_tom_kakie_my_horoshie'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)