from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Post, Category, Comment
from .mixin import DraftDispatchMixin
from .forms import CommentForm

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all().order_by('-pub_date')
        return context
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect(self.object.get_absolute_url())
        return self.get(request, *args, **kwargs)

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
    
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
