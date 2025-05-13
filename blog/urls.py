from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:post_id>/comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('post/<int:post_id>/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]