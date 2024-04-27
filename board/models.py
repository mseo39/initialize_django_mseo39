from django.db import models
from user.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20, null=False)
    
    def __str__(self):
        return self.name

"""
auto_now_add : 필드가 처음 생성될 때만 현재 날짜와 시간을 설정
auto_now     : 모델이 저장될 때마다 갱신된 날짜와 시간을 설정
"""
class Post(models.Model):
    category = models.ForeignKey(Category, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=300, null=False)
    created_date = models.DateField(auto_now=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    # related_name : 역참조를 통해 연결된 객체를 가져올 때 사용할 속성의 이름 정의
    # 즉, 연결된 모든 댓글을 쉽게 가져오기 위해
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    
    def __str__(self):
        return f"{self.author.username} : {self.post.title}"