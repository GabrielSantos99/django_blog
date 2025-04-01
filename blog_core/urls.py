from django.urls import path
from .views import HomeView, PostDetailView, CategoryListView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('categoria/<slug:slug>/', CategoryListView.as_view(), name='category_list'),
]