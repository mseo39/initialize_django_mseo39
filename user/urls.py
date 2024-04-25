from django.urls import path
import user.views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('session_signup', user.views.session_signup, name='session_signup'),
    path('jwt_signin', user.views.jwt_signin, name='jwt_signin'),
    path('only_authenticated_user', user.views.only_authenticated_user, name='only_authenticated_user'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]