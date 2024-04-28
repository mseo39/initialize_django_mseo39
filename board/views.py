from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes

from .models import *
from .serializers import *

from rest_framework.permissions import IsAdminUser, SAFE_METHODS

# admin 계정만 쓰기 수정이 가능하고 나머지는 읽기만 가능
class IsAdminUserOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        is_admin = super(
            IsAdminUserOrReadOnly, 
            self).has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin

@authentication_classes([JWTAuthentication]) 
@permission_classes([IsAdminUserOrReadOnly])
class CategoryViewSet(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, category_id):
        def get_object(self,category_id):
            try:
                return Post.objects.filter(category__id=category_id)
            except Post.DoesNotExist:
                return None
        
        category = self.get_object(category_id)
        if category:
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class PostViewSet(APIView):
    def get_object(self,category_id):
        try:
            return Post.objects.filter(category_id=category_id)
        except Post.DoesNotExist:
            return None
        
    def get(self, request, category_id):
        posts=self.get_object(category_id)
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)
    
"""
@permission_classes : 권한을 누구에게 줄지
IsAuthenticated - 인증된 사용자에게만 허용
IsAdminUser - 관리자만 허용
IsAuthenticatedOrReadOnly 
- 인증된 사용자는 읽기 쓰기 모두 허용
- 인증되지 않은 사용자는 읽기만 가능
"""
@authentication_classes([JWTAuthentication]) 
@permission_classes([IsAuthenticatedOrReadOnly])
class PostDetailViewSet(APIView):
    
    def get_object(self, post_id):
        try:
            return Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return None

    def get(self, request, post_id):
        post = self.get_object(post_id)
        if post:
            serializer = PostSerializer(post)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request):
        request.data['author'] = request.user.id 
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, post_id):
        post = self.get_object(post_id)
        if post:
            if request.user.id == post.author.id:
                serializer = PostSerializer(post, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "You are not allowed"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, post_id):
        post = self.get_object(post_id)
        if post:
            if request.user.id == post.author.id:
                post.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "You are not allowed"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)