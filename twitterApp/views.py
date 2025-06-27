from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .models import Post, Like, Follow, Retweet

User = get_user_model()

def home(request):
    tweets = Post.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'tweets': tweets})

@login_required
def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    user_tweets = Post.objects.filter(user=user_profile).order_by('-created_at')
    user_retweets = Retweet.objects.filter(user=user_profile).select_related('tweet')
    is_following = Follow.objects.filter(follower=request.user, followed=user_profile).exists()
    context = {
        'user_profile': user_profile,
        'user_tweets': user_tweets,
        'user_retweets': user_retweets,
        'is_following': is_following
    }
    return render(request, 'profile.html', context)


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(request.user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            print(request.user)
            return render(request, 'login.html')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    print(request.user)
    return redirect('home')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'register.html')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )

        user.save()
        messages.success(request, "Registration successful!")
        return redirect('home')
    else:
        return render(request, 'register.html')


@login_required
def user_tweet(request):
    if request.method == "POST":
        tweet_content = request.POST.get('tweet')
        if tweet_content:
            tweet = Post(content=tweet_content, user=request.user)
            tweet.save()
            return redirect('home')
    return render(request, 'tweet.html')


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    try:
        like = Like.objects.get(user=request.user, tweet=post)
        like.delete()
        print('Like deleted')
    except Like.DoesNotExist:
        Like.objects.create(user=request.user, tweet=post)
        print('Liked!')
    return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirect to the referring URL or fallback to home

@login_required
def retweet(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    
    retweet = Retweet.objects.filter(user=user, tweet=post).first()

    if retweet:
        retweet.delete()
        print('Retweet NOT done!')
    else:
        Retweet.objects.create(user=user, tweet=post)  # Corrected here
        print('Retweet done!')

    return redirect('home')

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user == request.user:
        post.delete()
        return redirect('home')
    else:
        return HttpResponseForbidden("You do not have permission to delete this post.")

@login_required
def follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    if request.method == "POST":
        if request.user != user_to_follow:
            follow_instance, created = Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
            if created:
                messages.success(request, f"You are now following {user_to_follow.username}.")
            else:
                follow_instance.delete()  # Unfollow if already following
                messages.success(request, f"You have unfollowed {user_to_follow.username}.")
        else:
            messages.error(request, "You cannot follow yourself.")

    return redirect('user_profile', username=username)  # Redirect to the profile


