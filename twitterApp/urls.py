from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Home page - displays all tweets
    path('', views.home, name='home'),
    # User login page
    path('login/', views.user_login, name='login'),
    # User logout page
    path('logout/', views.user_logout, name='logout'),
    # User registration page
    path('register/', views.register, name='register'),
    # Page to create a new tweet
    path('tweet/', views.user_tweet, name='user_tweet'),
    # Like a post (toggles like)
    path('like/<int:post_id>/', views.like_post, name='like'),
    # Retweet a post (toggles retweet)
    path('retweet/<int:post_id>/', views.retweet, name='retweet'),
    # Delete a post
    path("delete/<int:post_id>/", views.delete_post, name="delete"),
    # User profile page
    path('profile/<str:username>/', views.profile, name='user_profile'),
    # Follow or unfollow a user
    path('follow/<str:username>/', views.follow, name='follow'),
    # Search for tweets or users
    path('search/', views.search, name='search'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
