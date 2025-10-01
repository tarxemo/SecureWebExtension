from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('api/check-url/', views.check_url, name='check_url'),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('manage_urls', views.manage_urls, name='manage_urls'),
    path('analytics', views.analytics, name='analytics'),
    path('logout', views.logout_user, name='logout'),
    path('add-restricted-url/', add_restricted_url, name='add_restricted_url'),
    path('restricted-url/edit/<int:pk>/', edit_restricted_url, name='edit_restricted_url'),
    path('restricted-url/delete/<int:pk>/', delete_restricted_url, name='delete_restricted_url'),
    path('delete-all/', delete_all_requested_urls, name='delete_all_requested_urls'),

    path('add-restricted-keyword/', views.add_restricted_keyword, name='add_restricted_keyword'),
    path('list-restricted-keywords/', views.list_restricted_keywords, name='list_restricted_keywords'),
]
