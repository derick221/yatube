from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import  user_passes_test
from .forms import GroupForm
from .models import Group, Post

def index(request):
    latest = list(Post.objects.select_related('author').values('author', 'author_id', 'id', 'pub_date', 'text').order_by("-pub_date")[:11])
    return render(request, "index.html", {"posts": latest})

def group_posts(request, slug):
    group = get_object_or_404(Group, slug = slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:12]
    return render(request, 'group.html', {'group': group, 'posts': posts})

def is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_admin)
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            return redirect('group_posts', slug=group.slug)
    else:
        form = GroupForm()
    return render(request, 'create_group.html', {'form': form})