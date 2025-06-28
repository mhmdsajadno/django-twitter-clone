from rest_framework import serializers
from twitterApp.models import Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'created_at', 'like_count', 'retweet_count']
        read_only_fields = ['id', 'user', 'created_at', 'like_count', 'retweet_count']
