from django.contrib import admin
from .models import Food
from .models import Food,Comment
admin.site.register(Food)

# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'food', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
admin.site.register(Comment, CommentAdmin)
