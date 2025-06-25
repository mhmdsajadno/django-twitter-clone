
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('tweet/', views.user_tweet, name='user_tweet'),
    path('like/<int:post_id>/', views.like_post, name='like'),
    path('retweet/<int:post_id>/', views.retweet, name='retweet'),
    path('profile/<str:username>/', views.profile, name='user_profile'),
    path('follow/<str:username>/', views.follow, name='follow'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)