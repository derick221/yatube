from django import forms
from .models import Group, Post, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()
      
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'slug', 'description']
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['group', 'text', 'image']
    image = forms.ImageField(required=False)
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']