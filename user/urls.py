from django.urls import path
import user.views

urlpatterns = [
    path('session_signup', user.views.session_signup, name='session_signup'),
    path('jwt_signin', user.views.jwt_signin, name='jwt_signin'),
]