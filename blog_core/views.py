from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView
from .mixin import DraftDispatchMixin

class HomeView(ListView):
    model = Post
    template_name = "blog_core/home.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(status='published').order_by('-published_at')

class PostDetailView(DraftDispatchMixin, DetailView):
    model = Post
    template_name = 'blog_core/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(status='published')

