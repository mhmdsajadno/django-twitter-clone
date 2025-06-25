from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Profile(AbstractUser):
    bio = models.TextField(blank=True)
    website = models.URLField(max_length=200)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

import re
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.extract_and_add_hashtags()

    def extract_and_add_hashtags(self):
        hashtags = set(re.findall(r"#(\w+)", self.content))
        for tag in hashtags:
            hashtag_obj, _ = Hashtag.objects.get_or_create(name=tag.lower())
            self.hashtags.add(hashtag_obj)

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def retweet_count(self):
        return self.retweets.count()


class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    posts = models.ManyToManyField(Post, related_name='hashtags')

    def __str__(self):
        return f"#{self.name}"

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    tweet = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    
    class Meta:
        unique_together = ('user', 'tweet')

class Retweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='retweets')
    tweet = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='retweets')

    class Meta:
        unique_together = ('user','tweet')

class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='following',
        on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='followers',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('follower', 'followed')

# Uncomment when ready to implement commenting functionality
# class Comment(models.Model):
#     post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='commented_posts', on_delete=models.CASCADE)
#     content = models.TextField(max_length=280)
#     created_at = models.DateTimeField(auto_now_add=True)