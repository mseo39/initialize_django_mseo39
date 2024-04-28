from django.urls import path
from .views import *

urlpatterns = [
    path('categories', CategoryViewSet.as_view(), name='categories'),
]