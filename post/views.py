from django.shortcuts import render
from .models import Article, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def detail_category(request, id=None):
    category = Category.objects.get(id=id)
    context = {'category': category}
    return render(request, 'blog/detail_category.html', context)


def detail_article(request, id=None):
    article = Article.objects.get(id=id)
    context = {'article': article}
    return render(request, 'blog/detail_article.html', context)


def index_2(request):
    artiii = Article.objects.all()
    paginator = Paginator(artiii, 4)
    page = request.GET.get('page')
    try:
        artiii = paginator.page(page)
    except EmptyPage:
        artiii = paginator.page(1)
    except PageNotAnInteger:
        artiii = paginator.page(1)
    context = {'artiii': artiii}
    return render(request, 'blog/index_2.html', context)

