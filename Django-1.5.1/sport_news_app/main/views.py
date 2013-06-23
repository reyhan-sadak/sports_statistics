# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import Http404
from main.models import SportNewsMainCategory, SportNewsCategory, SportNews, SportNewsComment, NEWS_PRIO
from SportNewsApp.navigationBar import getNavigationBar
from SportNewsApp.sideBar import getSideBar
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.models import User
from test.test_iterlen import len
import re
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

def getUseInfo(request):
    user_info = {}
    if request.user.is_authenticated():
        user = request.user
        user_info['first_name'] = user.first_name
    return user_info

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
            
    return render(request,
                  'main/index.html', {'user_info': getUseInfo(request), 'navigationBar': getNavigationBar(),'side_bar': getSideBar(), 'first_news': first_news, 'main_news': main_news, 'other_news': other_news,},
                  context_instance=RequestContext(request)
                  )

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
    return render(request,
                  'main/category.html', {'user_info': getUseInfo(request), 'navigationBar': getNavigationBar(),'side_bar': getSideBar(int(category_id)), 'category_name': category_name, 'news_to_show': news_to_show,},
                  context_instance=RequestContext(request))

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
    return render(request,
                  'main/subCategory.html', {'user_info': getUseInfo(request), 'navigationBar': getNavigationBar(),'side_bar': getSideBar(int(category_id)), 'sub_category_name': sub_category_name, 'news_to_show': news_to_show,},
                  context_instance=RequestContext(request))

def news(request, news_id):
    comment_to_answer_id = '-1'
    if request.method == 'POST' and 'comment_to_answer_id' in request.POST:
        comment_to_answer_id = request.POST['comment_to_answer_id']
        comment_to_answer_id = comment_to_answer_id[:-1]
    try:
        news = SportNews.objects.get(pk=news_id)
    except SportNews.DoesNotExist:
        raise Http404
    photoUrl = '/media/' + str(news.photo)
    category_id = news.category.mainCategory.id
    comments = SportNewsComment.objects.filter(news=news).order_by('-created_at')
    comments_to_show = []
    for comment in comments:
        comment_to_show = {}
        comment_to_show['id'] = comment.id
        comment_to_show['created_at'] = comment.created_at
        comment_to_show['comment_number'] = comment.comment_number
        comment_to_show['user_username'] = comment.user.username
        comment_to_show['user_first_name'] = comment.user.first_name
        comment_to_show['user_last_name'] = comment.user.last_name
        comment_to_show['title'] = comment.title
        comment_to_show['text'] = comment.text
        comment_to_show['root_comment'] = comment.root_comment
        comments_to_show.append(comment_to_show)
    return render(request,
                  'main/news.html', {'user_info': getUseInfo(request), 'navigationBar': getNavigationBar(),'side_bar': getSideBar(category_id), 'news_id': news_id, 'news_title': news.title, 'news_text': news.text, 'photo': photoUrl, 'comments_to_show': comments_to_show, 'comment_to_answer_id': int(comment_to_answer_id)},
                  context_instance=RequestContext(request))

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        fromPath = request.POST['fromPath']
        fromPath = fromPath[:-1]
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(fromPath)
            else:
                return HttpResponse('Your user is not active')
        else:
            return HttpResponse('Your user name and password did not match!')
    else:
        return render(request, 'main/login.html')

def logout_view(request):
    fromPath = '/'
    if request.method == 'POST':
        fromPath = request.POST['fromPath']
        fromPath = fromPath[:-1]
    logout(request)
    return HttpResponseRedirect(fromPath)

def getEmptyFieldsSignUpErrors(request):
    signUpErrors = {}
    if 'username_create' not in request.POST or request.POST['username_create'] == '':
        signUpErrors['username_create'] = 'This field is mandatory'
    if 'password_create' not in request.POST or request.POST['password_create'] == '':
        signUpErrors['password_create'] = 'This field is mandatory'
    if 'confirm_password' not in request.POST or request.POST['confirm_password'] == '':
        signUpErrors['confirm_password'] = 'This field is mandatory'
    if 'first_name'  not in request.POST or request.POST['first_name'] == '':
        signUpErrors['first_name'] = 'This field is mandatory'
    if 'last_name' not in request.POST or request.POST['last_name'] == '':
        signUpErrors['last_name'] = 'This field is mandatory'
    if 'email' not in request.POST or request.POST['email'] == '':
        signUpErrors['email'] = 'This field is mandatory'
    return signUpErrors

def checkIfUserNameAlreadyExists(username):
    users = User.objects.filter(username=username)
    if len(users) > 0:
        return True;
    else:
        return False

def checkIfStringContainsDigit(string):
    pattern = r'\S*\d\S*'
    return bool(re.search(pattern, string))

def CheckIfStringContainsCapitalLetter(string):
    pattern = r'\S*[A-Z]\S*'
    return bool(re.search(pattern, string))

def checkIfPasswordIsValid(password):
    if len(password) < 10:
        return False
    elif not checkIfStringContainsDigit(password):
        return False
    elif not CheckIfStringContainsCapitalLetter(password):
        return False
    else:
        return True

def checkIfPasswordMatch(password1, password2):
    return password1 == password2

def checkIfEmailisValid(email):
    pattern = r'\S*@\S*\.\S*'
    return bool(re.search(pattern, email))

def create_account(request):
    signUpErrors = {}
    if request.method == 'POST':
        signUpErrors = getEmptyFieldsSignUpErrors(request)
        username = request.POST['username_create']
        password = request.POST['password_create']
        confirm_password = request.POST['confirm_password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        if username != '':
            if checkIfUserNameAlreadyExists(username):
                signUpErrors['username_create'] = 'User name already exists'
                return render(request, 'main/signup.html', {'user_info': getUseInfo(request), 'navigationBar': getNavigationBar(), 'signUpErrors': signUpErrors,})
            if not checkIfPasswordIsValid(password):
                signUpErrors['password_create'] = 'Your password did not meet the limitations.'
                return render(request, 'main/signup.html', {'user_info': getUseInfo(request), 'navigationBar': getNavigationBar(), 'signUpErrors': signUpErrors,})
            if not checkIfPasswordMatch(password, confirm_password):
                signUpErrors['confirm_password'] = 'The passwords did not match'
                return render(request, 'main/signup.html', {'user_info': getUseInfo(request), 'navigationBar': getNavigationBar(), 'signUpErrors': signUpErrors,})
            if first_name == '':
                return render(request, 'main/signup.html', {'user_info': getUseInfo(request), 'navigationBar': getNavigationBar(), 'signUpErrors': signUpErrors,})
            if last_name == '':
                return render(request, 'main/signup.html', {'user_info': getUseInfo(request), 'navigationBar': getNavigationBar(), 'signUpErrors': signUpErrors,})
            if not checkIfEmailisValid(email):
                signUpErrors['email'] = 'The email is not valid'
                return render(request, 'main/signup.html', {'user_info': getUseInfo(request), 'navigationBar': getNavigationBar(), 'signUpErrors': signUpErrors,})
            new_user = User()
            new_user.username = username
            new_user.set_password(password)
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.email = email
            new_user.save()
            authenticated_user = authenticate(username=username, password=password)
            login(request, authenticated_user)
            return HttpResponseRedirect('/')
    else:
        return render(request, 'main/signup.html', {'user_info': getUseInfo(request), 'navigationBar': getNavigationBar(), 'signUpErrors': signUpErrors,})

def search_news(request):
    search_word = ''
    if request.method == 'GET':
        search_word = request.GET['search_text']
    elif request.method == 'POST':
        search_word = request.POST['search_text']
    searched_news = SportNews.objects.filter(Q(title__icontains=search_word) | Q(text__icontains=search_word) | Q(category__name__icontains=search_word))
    news_to_show = []
    for news in searched_news:
        newsItem = []
        newsItem.append(news.id)
        newsItem.append(news.photo)
        newsItem.append(news.title)
        news_to_show.append(newsItem)
    return render(request, 'main/search_news.html', {'search_word': search_word,'user_info': getUseInfo(request), 'navigationBar': getNavigationBar(),'side_bar': getSideBar(int()), 'news_to_show': news_to_show,})

@login_required
def comment_news(request):
    if request.method == 'POST':
        fromPath = request.POST['fromPath']
        fromPath = fromPath[:-1]
        news_id = request.POST['news_id']
        news_id = news_id[:-1]
        news = SportNews.objects.filter(id=news_id)
        new_comment_title = request.POST['commentTitle']
        new_comment_text = request.POST['comment']
        answer_to_comment_id = '-1'
        if 'answer_to_comment_id' in request.POST:
            answer_to_comment_id = request.POST['answer_to_comment_id']
            answer_to_comment_id = answer_to_comment_id[:-1]
        if news and new_comment_title != '' and new_comment_text != '':
            commented_new = news[0]
            new_comment = SportNewsComment()
            new_comment.title = new_comment_title
            new_comment.text = new_comment_text
            new_comment.news = commented_new
            new_comment.user = request.user
            if answer_to_comment_id != '':
                root_comment = SportNewsComment.objects.filter(id=answer_to_comment_id)
                if root_comment:
                    new_comment.root_comment = root_comment[0]
            new_comment.save()
        return HttpResponseRedirect(fromPath)
    else:
        return HttpResponseRedirect('/')

def info(request):
    return render(request, 'main/info.html', {'user_info': getUseInfo(request), 'navigationBar': getNavigationBar(),'side_bar': getSideBar(),},
                  context_instance=RequestContext(request))