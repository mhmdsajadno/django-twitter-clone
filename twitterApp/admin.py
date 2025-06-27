from django.contrib import admin
from .models import Profile, Post, Hashtag, Like, Retweet, Follow

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'bio', 'website', 'first_name', 'last_name')
    search_fields = ('username', 'email')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at', 'like_count', 'retweet_count')
    search_fields = ('content',)
    list_filter = ('created_at',)

@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'tweet')
    list_filter = ('user',)

@admin.register(Retweet)
class RetweetAdmin(admin.ModelAdmin):
    list_display = ('user', 'tweet')
    list_filter = ('user',)

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'followed')
    list_filter = ('follower',)

# Uncomment when ready to implement commenting functionality
# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('post', 'author', 'content', 'created_at')
#     list_filter = ('post', 'author')
