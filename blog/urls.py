
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail' ),
#path('post/<int:pk>/', views.RepliesListView.as_view(), name='post-replies' ),
]