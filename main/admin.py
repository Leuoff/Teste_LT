from django.contrib import admin
from .models import Developer, Article

@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'seniority', 'user')
    search_fields = ('name', 'email', 'skills')
    list_filter = ('seniority',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'published_at')
    search_fields = ('title', 'content')
    list_filter = ('published_at',)
    filter_horizontal = ('developers',)
    prepopulated_fields = {'slug': ('title',)}
