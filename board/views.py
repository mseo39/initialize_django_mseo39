from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes

from .models import *
from .serializers import *

from rest_framework.permissions import IsAdminUser, SAFE_METHODS

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
    
    @swagger_auto_schema(request_body=CategorySerializer)
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_object(self,category_id):
            try:
                return Category.objects.filter(pk=category_id)
            except Category.DoesNotExist:
                return None
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'category_id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description='삭제할 category ID',
                required=True
            )
        ],
        responses={
            204: 'successfully',
            404: 'Category not found'
        },
    )
    def delete(self, request, category_id):
        
        category = self.get_object(category_id)
        if category:
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

from rest_framework.pagination import PageNumberPagination  

class CustomPagination(PageNumberPagination):
    page_size = 5 # 한번에 가져올 데이터 수
    page_query_param = 'page' # url 파라미터로 사용할 값
    page_size_query_param = 'limit' # 페이지당 가져올 데이터 항목 수

class PostViewSet(APIView):
    pagination_class = PageNumberPagination
    
    def get_object(self,category_id):
        try:
            return Post.objects.filter(category_id=category_id)
        except Post.DoesNotExist:
            return None
        
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'category_id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description='카테고리별 게시물 조회',
                required=True
            ),
            openapi.Parameter(
                'page',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='페이지 번호',
                required=False,
            ),
            openapi.Parameter(
                'limit',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='필요한 데이터 개수',
                required=False,
            ),
        ],
        responses={200: 'successfully'},
    )
    def get(self, request, category_id):
        posts=self.get_object(category_id)
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostListSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

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
        
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'post_id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description='검색할 post ID',
                required=True
            )
        ],
        responses={
            200: 'successfully',
            404: 'Post not found'
        },
    )
    def get(self, request, post_id):
        post = self.get_object(post_id)
        if post:
            serializer = PostSerializer(post)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
        request_body=PostSerializer(),
        responses={
            201: 'successfully',
            400: 'Invalid data provided'
        },
    )
    def post(self, request):
        request.data['author'] = request.user.id 
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'post_id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description='수정할 post ID',
                required=True
            )
        ],
        request_body=PostSerializer,
        responses={
            200: 'successfully',
            400: 'Invalid data provided',
            403: 'Forbidden: You are not allowed to update this post',
            404: 'Post not found'
        },
    )
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
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'post_id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description='삭제할 post ID',
                required=True
            )
        ],
        responses={
            204: 'successfully',
            403: 'Forbidden: You are not allowed to delete this post',
            404: 'Post not found'
        },
    )
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
        
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CommentViewSet(APIView):
    def get_object(self, comment_id):
        try:
            return Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return None
    
    @swagger_auto_schema(
        request_body=CommentSerializer,
        responses={
            201: 'successfully',
            400: 'Invalid data provided'
        },
    )
    def post(self, request):
        request.data['author'] = request.user.id 
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'comment_id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description='삭제할 comment ID',
                required=True
            )
        ],
        responses={
            204: 'successfully',
            403: 'Forbidden: You are not allowed to delete this comment',
            404: 'Comment not found'
        },
    )
    def delete(self, request, comment_id):
        comment = self.get_object(comment_id)
        if comment:
            # 토큰에 담긴 사용자 정보와 댓글 작성자 정보를 비교하여 일치하는지 확인
            if request.user.id == comment.author.id:
                comment.delete()
                return Response({"message": "successfully."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "You are not allowed"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)