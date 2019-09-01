from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
class Food(models.Model):
    STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    )
    title = models.CharField(max_length=20)
    slug = models.SlugField(max_length=30, unique_for_date='publish')
    author = models.ForeignKey(User,
    related_name='foodblog_food',
    on_delete=models.CASCADE,)
    desc = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
    choices=STATUS_CHOICES,
    default='draft')
    class Meta:
        ordering = ('-publish',)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('foodblog:food_detail',
    args=[self.publish.year,
    self.publish.strftime('%m'),
    self.publish.strftime('%d'),
    self.slug]
    )

class Comment(models.Model):
    food = models.ForeignKey(Food,
    related_name='comments',
    on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.food)
