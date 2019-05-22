from django.shortcuts import render
from django.http import HttpResponse,Http404
from pineBook.forms import loginForm,registerForm
from book.models import *
from friend.models import *
from django.contrib import auth
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from django.core import serializers
from django.core.mail import send_mail
import json
import uuid



vcode_changepwd = {}
vcode_register = {}

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
    print(vcode_register)
    if request.method == 'POST':
        ret = {"status": "ERROR", "errors": None}
        form = registerForm(request.POST)
        if form.is_valid() and request.POST.get('vcode') == vcode_register[request.POST.get('email')] and request.POST.get('vcode'):
            cd = form.cleaned_data
            user = User.objects.create_user(username=cd["username"], password=cd["password"], email=cd["email"])
            reader = Reader(user=user
                            , telephone=cd["telephone"]
                            , city=cd["city"]
                            , school=cd["school"])
            reader.save()
            ret["status"] = "OK"
        else:
            ret["verify"] = "验证码错误，请重新输入"
            ret["errors"] = form.errors
        return JsonResponse(ret)
    else:
        form = registerForm()
        return render(request,'register.html',{'regform':form,'loginform': loginForm()})

def personal(request):
    return Http404


def sendemail(request):
    print(request.path)
    email = request.POST.get('Email', None)
    vcode = uuid.uuid4().hex[:4]
    message='尊敬的用户'+email+',您好：'\
            +'\n您的验证码是：'+str(vcode)\
            +'\n本邮件由系统自动发送，请勿直接回复！'\
            +'\n感谢您的访问，祝您使用愉快！'
    try:
        user = User.objects.get(email=email)
    except:
        user = None
    if not user and request.path=="/backpwd":
        return JsonResponse({'status': '用户不存在!'})
    res = send_mail(subject='pineBook--邮箱验证', message=message, from_email='松书<1170998607@qq.com>',recipient_list=[email], fail_silently=False)
    context={}
    if(res==0):
        context = {'status': '失败'}
    elif(res==1):
        context = {'status': '成功'}
        if(request.path=="/register/sendemail/"):
            vcode_register[email]=vcode
        elif(request.path=="/changepwd/sendemail"):
            vcode_changepwd[email]=vcode
    print(vcode_register)
    return JsonResponse(context)


