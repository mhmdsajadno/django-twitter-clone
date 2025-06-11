
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('tweet/', views.user_tweet, name='user_tweet'),
    path('like/<int:post_id>/', views.like_post, name='like'),
    path('retweet/', views.retweet, name='retweet'),
    path('profile/<str:username>/', views.profile, name='user_profile'),
    path('follow/<str:username>/', views.follow, name='follow'),
]
