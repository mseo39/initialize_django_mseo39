from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user.jwt_claim_serializer import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import *

# Create your views here.

@api_view(['POST'])
def session_signup(request):
    if request.method == 'POST':
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            # validated_data: 유효성 검사를 통과한 데이터를 의미
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.save()
            return Response({'message': 'successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def jwt_signin(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = User.objects.get(username=username)
        # 비밀번호 검증
        if check_password(password, user.password):
            access = CustomTokenObtainPairSerializer.get_token(user).access_token
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(access),
                'refresh_token': str(refresh)
            }, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)