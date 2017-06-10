from django.contrib import admin
from .models import Article, Category
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
