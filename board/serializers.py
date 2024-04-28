from rest_framework import serializers
from board.models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
        
class CommentSerializer(serializers.ModelSerializer):
    
    def to_representation(self, instance):
        res = super().to_representation(instance)
        res.update({'author': UserSerializer(instance.author).data})
        return res
    
    class Meta:
        model = Comment
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
        
class PostSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = '__all__'
        
    def update(self, instance, validated_data):
        instance.category = validated_data.get('category', instance.category)
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
    
    #응답으로 사용자 이름이 전달되기 위해
    def to_representation(self, instance):
        res = super().to_representation(instance)
        res.update({'author': UserSerializer(instance.author).data})
        return res
        
    
class PostListSerializer(serializers.ModelSerializer):
     class Meta :
        model = Post
        fields = ('id', 'title', 'created_date',  'modified_date', )