from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import re

#Extending the base User model to include profile imformation.
class Profile(AbstractUser):
    """
    Extends the default Django User model to include additional profile information.
    """
    bio = models.TextField(blank=True, help_text="A short biography about the user.")
    website = models.URLField(max_length=200, blank=True, help_text="The user's personal website URL.")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, help_text="The user's profile picture.")


class Post(models.Model):
    """
    Represents a user's post (tweet).
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts', help_text="The user who created the post.")
    content = models.TextField(max_length=280, help_text="The content of the post (max 280 characters).")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time the post was created.")

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to extract and add hashtags when a post is saved.
        """
        super().save(*args, **kwargs)
        self.extract_and_add_hashtags()

    def extract_and_add_hashtags(self):
        """
        Extracts hashtags from the post content and associates them with the post.
        """
        hashtags = set(re.findall(r"#(\w+)", self.content))
        for tag in hashtags:
            hashtag_obj, _ = Hashtag.objects.get_or_create(name=tag.lower())
            self.hashtags.add(hashtag_obj)

    @property
    def like_count(self):
        """
        Returns the number of likes for this post.
        """
        return self.likes.count()

    @property
    def retweet_count(self):
        """
        Returns the number of retweets for this post.
        """
        return self.retweets.count()


class Hashtag(models.Model):
    """
    Represents a hashtag.  Stores unique hashtag names.
    """
    name = models.CharField(max_length=100, unique=True, help_text="The name of the hashtag (e.g., 'django').  Must be unique.")
    posts = models.ManyToManyField(Post, related_name='hashtags', help_text="The posts that use this hashtag.")

    def __str__(self):
        return f"#{self.name}"

class Like(models.Model):
    """
    Represents a user liking a post.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes', help_text="The user who liked the post.")
    tweet = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', help_text="The post that was liked.")
    
    class Meta:
        """
        Ensures that a user can only like a post once.
        """
        unique_together = ('user', 'tweet')

class Retweet(models.Model):
    """
    Represents a user retweeting a post.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='retweets', help_text="The user who retweeted the post.")
    tweet = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='retweets', help_text="The post that was retweeted.")

    class Meta:
        """
        Ensures that a user can only retweet a post once.
        """
        unique_together = ('user','tweet')

class Follow(models.Model):
    """
    Represents a user following another user.
    """
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='following',
        on_delete=models.CASCADE,
        help_text="The user who is following."
    )
    followed = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='followers',
        on_delete=models.CASCADE,
        help_text="The user who is being followed."
    )

    class Meta:
        """
        Ensures that a user can only follow another user once.
        """
        unique_together = ('follower', 'followed')

# Uncomment when ready to implement commenting functionality
# class Comment(models.Model):
#     post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='commented_posts', on_delete=models.CASCADE)
#     content = models.TextField(max_length=280)
#     created_at = models.DateTimeField(auto_now_add=True)
