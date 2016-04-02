from django.contrib import admin
from django import forms

from blog.models import Article

'''
class ArticleInLine(admin.StackedInline):
    model = Comments
    fields = ['comments_user', 'comments_text', 'comments_date']
    extra = 2
'''
class ArticleAdmin(admin.ModelAdmin):
    published = forms.CheckboxInput()

    fields = ['article_user', 'article_title','article_date_add','published', 'article_text', 'article_image']
    list_display = ['article_title', 'article_date_add','article_date_update', 'article_user', 'publish']#, 'bit']
    #inlines = [ArticleInLine]
    list_filter = ['article_date_add', 'article_user']


admin.site.register(Article, ArticleAdmin)

