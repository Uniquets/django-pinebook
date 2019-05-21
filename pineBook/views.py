from django.shortcuts import render
from django.http import HttpResponse,Http404
from pineBook.forms import loginForm,registerForm
from book.models import *
from friend.models import *
from django.contrib import auth
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from django.core import serializers
import json


def homepage(request):
    print('emter')
    if request.method == 'GET':
        return render(request, 'index.html')
    ret = {"status": "NG", "msg": None}
    form = loginForm(request.POST)
    if form.is_valid():
        print("entervalid")
        cd = form.cleaned_data
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = auth.authenticate(username=username,password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            ret["status"] = "OK"
            return JsonResponse(ret)
        else:
            ret["status"] = "ERROR"
            ret["msg"] = {"other": "用户名或密码不正确"}
            return JsonResponse(ret)
    else:
        ret["status"] = "ERROR"
        ret["msg"] = form.errors
        return JsonResponse(ret)

def getdict(books):    #将查询到的书集合转换为格式{id:{name:xxx,author:xxx}}的字典
    rackdic = {}
    books = serializers.serialize("json", books)
    print(books)
    books = json.loads(books)
    for book in books:
        rackdic[book['pk']] = {'name': book['fields']['name'] ,
                               'author': Author.objects.get(id=book['fields']['author']).name,
                               'cover': book['fields']['cover']}
    print(rackdic)
    return rackdic

def getbooksfromAuthor(txt):
    books = set()
    for author in Author.objects.filter(name__contains=txt):
        for book in author.author_book.all():
            books.add(book)
    return books

def getrack(request):
    data={}
    print(request.GET.get('racktype'))
    if request.method == 'GET' : #通过ajax.GET请求渲染书架，判断当前登陆的用户的所在地，学校，渲染出本校书架，同城书架，个人书架
        if request.user.is_authenticated:
            if request.GET.get("racktype") == "city":
                city = City.objects.get(name = Reader.objects.get(user_id=request.user.id).city)
                books = city.city_book.all()
                books = getdict(books)
                data['status'] = 'online'
                data['city'] = Reader.objects.get(user_id=request.user.id).city
                data['books'] = books
                return JsonResponse(data)
            elif request.GET.get("racktype") == "school":
                school = School.objects.get(name = Reader.objects.get(user_id=request.user.id).school)
                books = school.school_book.all()
                books = getdict(books)
                data['status'] = 'online'
                data['school'] = Reader.objects.get(user_id=request.user.id).school
                data['books'] = books
                return JsonResponse(data)
        else:
                books = Book.objects.filter(city=1)
                books = getdict(books)
                data['city'] = '成都'
                data['status'] = 'offline'
                data['books'] = books
                return JsonResponse(data)
    elif request.method == 'POST': #通过ajax.POST提交筛选项，直接筛选出对应的书籍进行渲染书架
        data["books"]={}
        txt = request.POST.get('filtertxt')
        option = request.POST.getlist('option')
        nameset = Book.objects.filter(name__contains=txt)#Book.objects.filter(name__contains='白')
        authorset = getbooksfromAuthor(txt)
        if 'name' in option and nameset:
            data["books"].update(getdict(nameset))
        if 'author' in option and authorset:
            data["books"].update(getdict(authorset))
        data['status']='filter'
        return JsonResponse(data)

def showbook(request):
    if request.method == 'GET' and request.GET.get('id'):
        temp = Book.objects.get(id=request.GET.get('id'))

        book = {
            'name': temp.name,
            'owner': Reader.objects.get(id=temp.owner_id).user.username,
            'author': Author.objects.get(id=temp.author_id).name,
            'press': Press.objects.get(id=temp.press_id).name,
            'school': School.objects.get(id=temp.school_id).name,
            'city': City.objects.get(id=temp.city_id).name,
            'cover': temp.cover.url,
            'intro': temp.intro
                }
        return JsonResponse(book)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def register(request):
    print(request.POST.get('email'))
    if request.method == 'POST':
        ret = {"status": "ERROR", "errors": None}
        form = registerForm(request.POST)
        print(request.POST)
        print(form.errors)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(username=cd["username"], password=cd["password"], email=cd["email"])
            reader = Reader(user=user
                            , sex=cd["sex"]
                            , telephone=cd["telephone"]
                            , city=cd["city"]
                            , school=cd["school"]
                            , grade=cd["grade"])
            reader.save()
            ret["status"] = "OK"
        else:
            ret["errors"] = form.errors
            print(type(form.errors))
        return JsonResponse(ret)
    else:
        form = registerForm()
        return render(request,'register.html',{'regform':form,'loginform': loginForm()})

def personal(request):
    return Http404


