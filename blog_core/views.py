from django.shortcuts import get_object_or_404
from .models import Post, Category
from django.views.generic import ListView, DetailView
from .mixin import DraftDispatchMixin

class HomeView(ListView):
    model = Post
    template_name = 'blog_core/home.html'
    context_object_name = 'posts'
    paginate_by = 1
    queryset = Post.objects.filter(status='published').order_by('-published_at')

class PostDetailView(DraftDispatchMixin, DetailView):
    model = Post
    template_name = 'blog_core/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(status='published')

class CategoryListView(ListView):
    model = Post
    template_name = 'blog_core/category_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.categories = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(status='published', categories=self.categories).order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.categories
        return context
