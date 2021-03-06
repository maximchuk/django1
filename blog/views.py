from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, render_to_response
from django.http import Http404, HttpResponse
from django.template.context_processors import csrf
from comments.forms import CommentForm
from comments.models import Comment
from blog.models import Article, Category
from django.contrib import auth
from django.core.paginator import Paginator, InvalidPage, PageNotAnInteger, EmptyPage


def home(request):
    articles =Article.objects.filter(is_publish=1)
    paginator = Paginator(articles, 10)
    try:
        page_num = request.GET.get('page')
    except KeyError:
        page_num = 1

    try:
        articles = paginator.page(page_num)
    except InvalidPage:
        articles = paginator.page(1)

    args= {}
    args.update(csrf(request))
    args['articles'] = articles
    args['username'] = auth.get_user(request).username
    return render(request, 'blog/home.html', args)

'''
    context = {
        'articles': articles,
        'username': auth.get_user(request).username
    }
    return render(request, 'blog/home.html', context)
'''

def show_article(request, article_id):
    comment_form = CommentForm
    #pagination comments
    comments = Comment.objects.filter(comment_article_id=article_id)
    paginator = Paginator(comments, 3)
    try:
        page_num = request.GET.get('page')
    except KeyError:
        page_num = 1

    try:
        comments = paginator.page(page_num)
    except InvalidPage:
        comments = paginator.page(1)
    #except EmptyPage:
      #  comments = paginator.page(paginator.num_pages)
    # end pagination comments
    args ={}
    args.update(csrf(request))
    args['article'] = Article.objects.get(id=article_id)
    args['comments'] = comments
    args['form'] = comment_form
    args['username'] = auth.get_user(request).username
    return render(request, 'blog/article.html', args)

def pag_comm(request, comm_num = 1):
    comments = Comment.objects.all()
    current_comm = Paginator(comments, 2)
    args = {}
    args['comments'] = current_comm.page(comm_num)
    return render_to_response('blog/article.html', args)

def add_like(request, article_id):
    try:
        if article_id in request.COOKIES:
            return_path = request.META.get('HTTP_REFERER', '/')
            return redirect(return_path)
        else:
            article = Article.objects.get(id = article_id)
            article.article_likes += 1
            article.save()
            return_path = request.META.get('HTTP_REFERER', '/')
            response = redirect(return_path)
            response.set_cookie(article_id, 'like')
            return response
    except ObjectDoesNotExist:
        raise Http404
    return redirect('/')

def add_dislike(request, article_id):
    try:
        if article_id in request.COOKIES:
            return_path = request.META.get('HTTP_REFERER', '/')
            return redirect(return_path)
        else:
            article = Article.objects.get(id = article_id)
            article.article_dislikes += 1
            article.save()
            return_path = request.META.get('HTTP_REFERER', '/')
            response = redirect(return_path)
            response.set_cookie(article_id, 'dislike')
            return response
    except ObjectDoesNotExist:
        raise Http404
    return redirect('/')


def add_comment(request, article_id):
    if request.POST and ("pause", not request.session):
        form = CommentForm(request.POST)
        return_path = request.META.get('HTTP_REFERER', '/')
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comment_user = request.user
            comment.comment_article = Article.objects.get(id = article_id)
            form.save()
            request.session.set_expiry(600)
            request.session['pause'] = True
    return  redirect(return_path)

def about(request):
    return render(request, 'blog/about.html')

def ajax(request, article_id):
    response = HttpResponse()
    response['Content-Typ'] = "text/javascript"
    response.write(serializers.serialize("json", Article.objects.filter(pk__gt = article_id, is_publish=1)))
    return response
