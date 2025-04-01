from django.contrib import admin
from .models import Category, Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'published_at')
    list_filter = ('status', 'published_at', 'author')
    search_fields = ('title', 'content', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = ('published_at')
    ordering = ('-published_at',)
    list_editable = ('status',)

admin.site.register(Category)
admin.site.register(Comment)
