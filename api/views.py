from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from twitterApp.models import Post
from api.serializer import UserSerializer
from django.contrib.auth.decorators import login_required

@login_required
@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def post(request):
    if request.method == "GET":
        posts = Post.objects.all()
        serializer = UserSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # associate with the logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
