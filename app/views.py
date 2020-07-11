"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from .models import Article,Disscuss
from django.core.paginator import Paginator
from django.shortcuts import redirect

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

# 视图函数
def article_content(request):
    article = Article.objects.all()[0]
    article_id = article.article_id
    title = article.title
    brief_content = article.brief_content
    content = article.content
    publish_date = article.date
    return_str = 'article_id:%s,title:%s,brief_content:%s,' \
                 'content:%s,publish_date:%s' % (article_id, title,
                                                 brief_content, content,
                                                 publish_date)
    return HttpResponse(return_str)


def get_index_page(request):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    all_article = Article.objects.all()
    top5_article_list = Article.objects.order_by('-date')[:5]
    paginator = Paginator(all_article, 8)

    page_num = paginator.num_pages
    page_article_list = paginator.page(page)
    if page_article_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_article_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page
    return render(request, 'app/ind.html',
                  {
                      'article_list': page_article_list,
                      'page_num': range(1, page_num + 1),
                      'curr_page': page,
                      'next_page': next_page,
                      'previous': previous_page,
                      'top5_article_list': top5_article_list,
                      'page': page
                  })


def get_detail_page(request, article_id):
    all_article = Article.objects.all()
    all_dis = Disscuss.objects.all()
    disscuss = []
    print(type(all_article))
    print(all_article)
    curr_article = None
    previous_index = 0
    next_index = 0
    previous_article = None
    next_article = None
    for index, article in enumerate(all_article):
        if index == 0:
            previous_index = 0
            next_index = index + 1
        elif index == len(all_article) - 1:
            previous_index = index - 1
            next_index = index
        else:
            previous_index = index - 1
            next_index = index + 1
        if article.article_id == article_id:
            curr_article = article
            for i in all_dis:
                if i.article_id == article_id:
                    disscuss.append(i.content)
            previous_article = all_article[previous_index]
            next_article = all_article[next_index]
            break
    section_list = curr_article.content.split('\n')
    return render(request, 'app/detail.html', {
        'curr_article': curr_article,
        'section_list': section_list,
        'previous_article': previous_article,
        'next_article': next_article,
        'disscuss':disscuss,
        'id':article_id
    })
def add_dis(request, article_id):
    article_id = int(article_id)
    if request.method =="POST":
        content = request.POST['content']
        dis = Disscuss(article_id = article_id,content = content)
        dis.save()
        print(dis)
    return  redirect("/blog/detail/"+str(article_id)) 
def add_blog(request):
    if request.method =="POST":
        title = request.POST['title']
        brief_content = request.POST['content'][0:20]
        content = request.POST['content']
    article = Article(title=title,brief_content = brief_content,content =content)
    article.save()
    return  redirect("/blog/index") 