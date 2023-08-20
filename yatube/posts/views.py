from rest_framework import generics
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import  user_passes_test, login_required
from django.views.generic.edit import CreateView
from posts.permissions import IsAuthorOrReadOnly
from .forms import GroupForm, PostForm, CommentForm
from .models import Group, Post, User, UserProfile, Comment, Follow
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import logging
from django.db import IntegrityError
from django.db.utils import OperationalError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly] 


logger = logging.getLogger(__name__)

def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.

    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    form = CommentForm()  # Создание экземпляра формы комментария
    return render(request, 'index.html', {'page': page, 'form': form, 'paginator': paginator})

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(post_list, 10)  # Показывать по 10 записей на странице.

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'group.html', {'group': group, 'posts': page})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration.html', {'form': form})

def is_admin(user):
    return user.is_authenticated and user.is_superuser
def group_view(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(post_list, 10)  # Показывать по 10 записей на странице.

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'group.html', {'group': group, 'posts': page})

@user_passes_test(is_admin)
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            return redirect('group_view', slug=group.slug)
    else:
        form = GroupForm()
    return render(request, 'create_group.html', {'form': form})

class PostView(CreateView):
    form_class = PostForm
    success_url = "/" 
    template_name = "new_post.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Учитываем загруженные файлы
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()

    return render(request, 'new_post.html', {'form': form})

@login_required
def post_edit(request, username, post_id):
    
    post = get_object_or_404(Post, id=post_id, author__username=username)
    if request.user != post.author:
        return redirect('post_detail', username=username, post_id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)  # Учитываем загруженные файлы
        if form.is_valid():
            form.save()
            return redirect('post_detail', username=username, post_id=post_id)
    else:
        form = PostForm(instance=post)

    return render(request, 'new_post.html', {'form': form})

def about_author(request):
    return render(request, 'about_author.html')

def about_technologies(request):
    return render(request, 'about_technologies.html')

def profile(request, username):
    user = get_object_or_404(User, username=username)
    
    # Получаем все посты, принадлежащие данному пользователю
    posts = Post.objects.filter(author=user).order_by('-pub_date')
    posts_count = posts.count()
    user_profile = get_object_or_404(UserProfile, user=user)
    followers_count = user_profile.followers.count()
    following_count = user_profile.following.count()
    
    return render(request, 'profile.html', {
        'user': user,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'posts_count': posts_count,
    })

    
@cache_page(20, key_prefix = 'page')
def post_view(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    comments = Comment.objects.filter(post=post)
    form = CommentForm()  # Создайте экземпляр вашей формы
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})

def post_detail(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    comments = post.comments.all()
    form = CommentForm()  # Здесь должно быть создание формы
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})

def page_not_found(request, exception):
    return render(request, 'misc/404.html', status=404)

def server_error(request):
    return render(request, 'misc/500.html', status=500)

def add_comment(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', username=username, post_id=post_id)
    else:
        form = CommentForm()
    return render(request, 'comments.html', {'form':form})

@login_required
def follow_index(request):
    following_profiles = request.user.userprofile.following.all()
    following_users = [profile.user for profile in following_profiles]
    posts = Post.objects.filter(author__in=following_users).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "follow.html", {"page": page, "paginator": paginator})

@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)

    if author == request.user:
        return redirect("profile", username=username)

    try:
        Follow.objects.get_or_create(user=request.user, author=author)
    except (IntegrityError, OperationalError) as e:
        logger.error(f"Error while following: {e}")

    return redirect("profile", username=username)

@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)

    try:
        Follow.objects.filter(user=request.user, author=author).delete()
    except (IntegrityError, OperationalError) as e:
        logger.error(f"Error while unfollowing: {e}")

    return redirect("profile", username=username)

@api_view(['GET', 'POST'])
def api_posts(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_posts_detail(request, id):
    post = get_object_or_404(Post, pk=id)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method in ['PUT', 'PATCH']:
        serializer = PostSerializer(post, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)