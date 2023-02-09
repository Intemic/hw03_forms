from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post

NUMBER_OF_LINES_ON_PAGE = 10

User = get_user_model()


def index(request: HttpRequest) -> HttpResponse:
    post_list = Post.objects.select_related('author', 'group').all()
    paginator = Paginator(post_list, NUMBER_OF_LINES_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }

    return render(request, 'posts/index.html', context)


def group_posts(request: HttpRequest, slug: str) -> HttpResponse:
    group = get_object_or_404(Group, slug=slug)
    posts_list = Post.objects.filter(group=group)
    paginator = Paginator(posts_list, NUMBER_OF_LINES_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_count = user.posts.count()
    post_list = Post.objects.filter(
        author=user).prefetch_related('author', 'group').all()
    paginator = Paginator(post_list, NUMBER_OF_LINES_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': user,
        'page_obj': page_obj,
        'post_count': post_count,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post_count = post.author.posts.count()
    context = {
        'post': post,
        'post_count': post_count,
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    groups = Group.objects.all()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(f'/profile/{post.author.username}/')

        context = {
            'form': form,
            'groups': groups
        }
        return render(request, 'posts/create_post.html', context)

    form = PostForm()
    context = {
        'form': form,
        'groups': groups,
    }
    return render(request, 'posts/create_post.html', context)


def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    groups = Group.objects.all()

    if not request.user.is_authenticated:
        return redirect(f'/posts/{post_id}')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(f'/posts/{post_id}')

        context = {
            'is_edit': True,
            'form': form,
            'groups': groups,
            'post': post,
        }

        return render(request, 'posts/create_post.html', context)

    form = PostForm(instance=post)
    context = {
        'is_edit': True,
        'form': form,
        'groups': groups,
        'post': post,
    }
    return render(request, 'posts/create_post.html', context)
