from django.urls import path
from .views import *

urlpatterns = [
    path('categories', CategoryViewSet.as_view(), name='categories'),
    path('posts/<int:category_id>', PostViewSet.as_view(), name='posts_category'),
]