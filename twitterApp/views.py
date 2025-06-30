from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .models import Post, Like, Follow, Retweet, Profile

User = get_user_model()

def home(request):
    """
    Displays all tweets on the home page, ordered by most recent first.
    """
    tweets = Post.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'tweets': tweets})

@login_required
def profile(request, username):
    """
    Displays a user's profile, including their tweets and retweets.

    Args:
        request: The HTTP request object.
        username: The username of the profile to display.
    """
    # Get the user's profile or return a 404 error
    user_profile = get_object_or_404(User, username=username)
    # Get the user's tweets, ordered by most recent first
    user_tweets = Post.objects.filter(user=user_profile).order_by('-created_at')
    #Get the User's retweets
    user_retweets = Retweet.objects.filter(user=user_profile).select_related('tweet')

    # Check if the currently logged-in user is following this profile
    is_following = Follow.objects.filter(follower=request.user, followed=user_profile).exists()

    context = {
        'user_profile': user_profile,
        'user_tweets': user_tweets,
        'user_retweets' : user_retweets,
        'is_following': is_following
    }
    return render(request, 'profile.html', context)


def user_login(request):
    """
    Handles user login.
    """
    if request.method == "POST":
        # Get username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in
            login(request, user)
            print(request.user) #Debug
            return redirect('home')
        else:
            # Display an error message if authentication fails
            messages.error(request, "Invalid username or password.")
            print(request.user) #Debug
            return render(request, 'login.html')
    # Render the login form if it's a GET request
    return render(request, 'login.html')

def user_logout(request):
    """
    Logs the user out.
    """
    logout(request)
    print(request.user) #Debug
    return redirect('home')

def register(request):
    """
    Handles user registration.
    """
    if request.method == "POST":
        # Get registration data from the form
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'register.html')

        # Create a new user
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
        # Render the registration form if it's a GET request
        return render(request, 'register.html')


@login_required
def user_tweet(request):
    """
    Handles the creation of a new tweet.  Requires the user to be logged in.
    """
    if request.method == "POST":
        # Get the tweet content from the form
        tweet_content = request.POST.get('tweet')
        if tweet_content:
            # Create a new tweet and save it to the database
            tweet = Post(content=tweet_content, user=request.user)
            tweet.save()
            return redirect('home')
    # Render the tweet form
    return render(request, 'tweet.html')


@login_required
def like_post(request, post_id):
    """
    Handles liking and unliking a post.  Requires the user to be logged in.
    """
    # Get the post or return a 404 error if it doesn't exist
    post = get_object_or_404(Post, id=post_id)
    try:
        # Try to get an existing like from the user on this post
        like = Like.objects.get(user=request.user, tweet=post)
        # If it exists, delete the like (unlike the post)
        like.delete()
        print('Like deleted') #Debug
    except Like.DoesNotExist:
        # If it doesn't exist, create a new like (like the post)
        Like.objects.create(user=request.user, tweet=post)
        print('Liked!') #Debug
    # Redirect to the previous page
    return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirect to the referring URL or fallback to home

@login_required
def retweet(request, post_id):
    """Handles User Retweets, toggles retweets

    Args:
        request (_type_): requestObject
        post_id (_type_): Post ID to search for specific post.
    """
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
    """Deletes Post by Post ID, Must be the Author

    Args:
        request (_type_): Request Object
        post_id (_type_): Numerical Post_ID
    """
    post = get_object_or_404(Post, id=post_id)
    if post.user == request.user:
        post.delete()
        return redirect('home')
    else:
        return HttpResponseForbidden("You do not have permission to delete this post.")

@login_required
def follow(request, username):
    """Handles following of Users, Allows toggle by Posting, Checks Auth

    Args:
        request (_type_): request Object
        username (_type_): Username of Target user.
    """
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

def search(request):
    query = request.GET.get('search', '')
    post_results = Post.objects.filter(content__icontains=query) if query else []
    user_results = Profile.objects.filter(username__icontains=query) if query else []
    return render(request, 'search.html', {
        'query': query,
        'tweets': post_results,
        'users': user_results,
    })