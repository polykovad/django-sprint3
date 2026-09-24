from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Post, Category

POSTS_ON_MAIN_PAGE = 5


def get_published_posts():
    """Базовый queryset опубликованных постов.

    Используется во всех view-функциях; к нему добавляются
    дополнительные фильтры, лимиты и сортировки по месту.
    """
    return (
        Post.objects
        .select_related('author', 'location', 'category')
        .filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        )
    )


def index(request):
    template = 'blog/index.html'
    post_list = get_published_posts()[:POSTS_ON_MAIN_PAGE]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    post = get_object_or_404(get_published_posts(), id=post_id)
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    post_list = get_published_posts().filter(category=category)
    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, template, context)
