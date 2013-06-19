# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404
from main.models import SportNewsMainCategory, SportNewsCategory, SportNews, NEWS_PRIO
from SportNewsApp.navigationBar import getNavigationBar
from SportNewsApp.sideBar import getSideBar

def index(request):
    first_news = []
    first_news_list = SportNews.objects.filter(priority='NEWS_MAIN').order_by('-created_at')
    if len(first_news_list) > 0:
        news_info = {}
        news_info['title'] = first_news_list[0].title
        news_info['img'] = '/media/' + str(first_news_list[0].photo)
        first_news.append(first_news_list[0].id)
        first_news.append(news_info)
    main_news = []
    for news_prio in NEWS_PRIO:
        if news_prio[0] != 'NEWS_NORMAL' and news_prio[0] != 'NEWS_MAIN':
            main_news_list = SportNews.objects.filter(priority=news_prio[0]).order_by('-created_at')
            if len(main_news_list) > 0:
                news_info = {}
                news_info['title'] = main_news_list[0].title
                news_info['img'] = '/media/' + str(main_news_list[0].photo)
                news = []
                news.append(main_news_list[0].id)
                news.append(news_info)
                main_news.append(news)
    
    other_news_list = SportNews.objects.all().order_by('-created_at')[:20]
    other_news = []
    for other in other_news_list:
        news = []
        news.append(other.id)
        news.append(other.photo)
        news.append(other.title)
        isItemInMainNews = False
        for mainNewsItem in main_news:
            if mainNewsItem[0] == news[0]:
                isItemInMainNews = True
        if not isItemInMainNews and first_news and other.id != first_news[0]:
            other_news.append(news)
            
    return render(request, 'main/index.html', {'navigationBar': getNavigationBar(),'side_bar': getSideBar(), 'first_news': first_news, 'main_news': main_news, 'other_news': other_news,})

def category(request, category_id):
    category = SportNewsMainCategory.objects.filter(id=category_id)
    category_news = SportNews.objects.filter(category__mainCategory=category).order_by('-created_at')
    category_name = ''
    if category:
        category_name = category[0].name
    news_to_show = []
    for news in category_news:
        newsItem = []
        newsItem.append(news.id)
        newsItem.append(news.photo)
        newsItem.append(news.title)
        news_to_show.append(newsItem)
    return render(request, 'main/category.html', {'navigationBar': getNavigationBar(),'side_bar': getSideBar(int(category_id)), 'category_name': category_name, 'news_to_show': news_to_show,})

def sub_category(request, category_id, subcategory_id):
    main_category = SportNewsMainCategory.objects.filter(id=category_id)
    sub_category = SportNewsCategory.objects.filter(mainCategory=main_category).filter(id=subcategory_id)
    sub_category_name = ''
    if sub_category:
        sub_category_name = sub_category[0].name
    sub_category_news = SportNews.objects.filter(category=sub_category).order_by('-created_at')
    news_to_show = []
    for news in sub_category_news:
        newsItem = []
        newsItem.append(news.id)
        newsItem.append(news.photo)
        newsItem.append(news.title)
        news_to_show.append(newsItem)
    return render(request, 'main/subCategory.html', {'navigationBar': getNavigationBar(),'side_bar': getSideBar(int(category_id)), 'sub_category_name': sub_category_name, 'news_to_show': news_to_show,})

def news(request, news_id):
    try:
        news = SportNews.objects.get(pk=news_id)
    except SportNews.DoesNotExist:
        raise Http404
    photoUrl = '/media/' + str(news.photo)
    category_id = news.category.mainCategory.id
    return render(request, 'main/news.html', {'navigationBar': getNavigationBar(),'side_bar': getSideBar(category_id), 'news_title': news.title, 'news_text': news.text, 'photo': photoUrl,})