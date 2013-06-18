# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404
from main.models import SportNewsMainCategory, SportNewsCategory, SportNews, NEWS_PRIO
from SportNewsApp.navigationBar import getNavigationBar
from SportNewsApp.sideBar import getSideBar

def index(request):
    first_news = []
    first_news_list = SportNews.objects.filter(priority='NEWS_MAIN1').order_by('-created_at')
    if len(first_news_list) > 0:
        news_info = {}
        news_info['title'] = first_news_list[0].title
        news_info['img'] = '/media/' + str(first_news_list[0].photo)
        first_news.append(first_news_list[0].id)
        first_news.append(news_info)
    main_news = {}
    for news_prio in NEWS_PRIO:
        if news_prio[0] != 'NEWS_NORMAL' and news_prio[0] != 'NEWS_MAIN5' and news_prio[0] != 'NEWS_MAIN1':
            main_news_list = SportNews.objects.filter(priority=news_prio[0]).order_by('-created_at')
            if len(main_news_list) > 0:
                news_info = {}
                news_info['title'] = main_news_list[0].title
                news_info['img'] = '/media/' + str(main_news_list[0].photo)
                main_news[main_news_list[0].id] = news_info
    
    other_news_list = SportNews.objects.all().order_by('-created_at')
    other_news = {}
    for other in other_news_list:
        if other.id not in main_news and other.id != first_news[0]:
            other_news[other.id] = other.title
            
    return render(request, 'main/index.html', {'navigationBar': getNavigationBar(),'side_bar': getSideBar(), 'first_news': first_news, 'main_news': main_news, 'other_news': other_news,})

def category(request, category_id):
    category = SportNewsMainCategory.objects.filter(id=category_id)
    category_news = SportNews.objects.filter(category__mainCategory=category)
    category_name = ''
    if category:
        category_name = category[0].name
    news_to_show = {}
    for news in category_news:
        news_to_show[news.id] = news.title
    return render(request, 'main/category.html', {'navigationBar': getNavigationBar(),'side_bar': getSideBar(int(category_id)), 'category_name': category_name, 'news_to_show': news_to_show,})

def sub_category(request, category_id, subcategory_id):
    main_category = SportNewsMainCategory.objects.filter(id=category_id)
    sub_category = SportNewsCategory.objects.filter(mainCategory=main_category).filter(id=subcategory_id)
    sub_category_name = ''
    if sub_category:
        sub_category_name = sub_category[0].name
    sub_category_news = SportNews.objects.filter(category=sub_category)
    news_to_show = {}
    for news in sub_category_news:
        news_to_show[news.id] = news.title
    return render(request, 'main/subCategory.html', {'navigationBar': getNavigationBar(),'side_bar': getSideBar(int(category_id)), 'sub_category_name': sub_category_name, 'news_to_show': news_to_show,})

def news(request, news_id):
    try:
        news = SportNews.objects.get(pk=news_id)
    except SportNews.DoesNotExist:
        raise Http404
    photoUrl = '/media/' + str(news.photo)
    category_id = news.category.mainCategory.id
    return render(request, 'main/news.html', {'navigationBar': getNavigationBar(),'side_bar': getSideBar(category_id), 'news_title': news.title, 'news_text': news.text, 'photo': photoUrl,})