from django.urls import path
import user.views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup', user.views.signup, name='signup'),
    path('session_signin', user.views.session_signin, name='session_signin'),
    path('bcrypt_signup', user.views.bcrypt_signup, name='bcrypt_signup'),
    path('bcrypt_signin', user.views.bcrypt_signin, name='bcrypt_signin'),
    path('jwt_signin', user.views.jwt_signin, name='jwt_signin'),
    path('only_authenticated_user', user.views.only_authenticated_user, name='only_authenticated_user'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]