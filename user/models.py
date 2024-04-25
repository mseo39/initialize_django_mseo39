from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=30)
    age = models.IntegerField
    
    class meta:
        db_table = 'user'