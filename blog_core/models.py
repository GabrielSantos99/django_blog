from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class Post(models.Model):
    STATUS_CHOICE = [('draft', 'Rascunho'), ('published', 'Publicado')]
    COVER_IMAGE_PATH = 'blog_covers/'

    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    summary = models.CharField(max_length=300, blank=True, default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default=STATUS_CHOICE[0][0])
    cover_image = models.ImageField(upload_to=COVER_IMAGE_PATH, blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def set_published_date(self):
        if self.published_at is None and self.status == self.STATUS_CHOICE[1][0]:
            self.published_at = timezone.now()

    def save(self, *args, **kwargs):
        self.set_published_date()
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    pub_date = models.DateTimeField('Data de publicação:', auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.author} em {self.post.title}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=300, blank=True)
    photo = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return f'Perfil de {self.user}'