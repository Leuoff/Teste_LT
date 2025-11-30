from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home_redirect, name='home'),
    path('signup/', views.signup, name='signup'),
    path('developers/', views.DeveloperListView.as_view(), name='developer_list'),
    path('developers/new/', views.DeveloperCreateView.as_view(), name='developer_create'),
    path('developers/<int:pk>/edit/', views.DeveloperUpdateView.as_view(), name='developer_update'),
    path('developers/<int:pk>/delete/', views.DeveloperDeleteView.as_view(), name='developer_delete'),
    path('articles/', views.ArticleListView.as_view(), name='article_list'),
    path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('articles/new/', views.ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', views.ArticleUpdateView.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
]
