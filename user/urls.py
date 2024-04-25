from django.urls import path
import user.views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup', user.views.signup, name='signup'),
    path('jwt_signin', user.views.jwt_signin, name='jwt_signin'),
    path('only_authenticated_user', user.views.only_authenticated_user, name='only_authenticated_user'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]