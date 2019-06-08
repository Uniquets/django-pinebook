from django.shortcuts import render
from django.http import HttpResponse,Http404
from pineBook.forms import loginForm,registerForm
from friend.models import *
from django.contrib import auth
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail
import uuid
from django.views.decorators.csrf import csrf_exempt
from datetime import *

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

def booklayer(request,id):
    if request.method == 'GET':
        temp = Book.objects.get(id=id)
        book = {
            'name': temp.name,
            'owner': temp.owner.username,
            'author': Author.objects.get(id=temp.author_id).name,
            'press': Press.objects.get(id=temp.press_id).name,
            'school': School.objects.get(id=temp.school_id).name,
            'city': City.objects.get(id=temp.city_id).name,
            'cover': temp.cover.url,
            'intro': temp.intro,
            'id':temp.id
        }
        message = []
        for m in temp.book_leavemessage.order_by('-sendtime'):
            message.append({
                'leaver':m.leaver.username,
                'sendtime':convertime(m.sendtime),
                'content':m.content,
                'status':m.status
            })
        if  request.user.id == temp.owner.id:
            isowner = True
        else:
            isowner = False
        unreadcount = temp.book_leavemessage.filter(status='未读').count()
        booklist = []
        for b in  request.user.user_book.all():
            booklist.append({'id':b.id,'title':b.name,'author':b.author})
        hasrequested = False
        if request.user.user_changerequest.filter(booka=temp):
            hasrequested = True
        return render(request, 'booklayer.html',
                      {'book':book,'message':message,
                       'isowner':isowner,'unread':unreadcount,
                       'booklist':booklist,'hasrequested':hasrequested})

def sendchangerequest(request):
    if request.method == 'POST':
        data =request.POST
        print(request.POST.get('booka'))
        try:
            c = Changerequest(
                            requester = request.user,
                            receiver = User.objects.get(username=data.get('receive')),
                            booka = Book.objects.get(id=data.get('booka')),
                            bookb = Book.objects.get(id=data.get('bookb')),
                            message = data.get('message'),
                            unread = User.objects.get(username=data.get('receive'))
                              )
            c.save()
            s = "OK"
        except Exception as e:
            raise e
    return JsonResponse({'status':s})

def searchuser(request):
    if request.method == 'POST':
        nametxt = request.POST.get('searchtxt')
        resultlist = {}
        for u in User.objects.filter(username__contains = nametxt):
            resultlist[u.id] = u.username
        print(resultlist)
        return JsonResponse(resultlist)


def getlist(books):    #将查询到的书集合转换为格式{id:{name:xxx,author:xxx}}的字典
    rackdic = []
    for book in books:
        rackdic.append({'id':book.id,
                        'name': book.name ,
                        'author': book.author.name,
                        'cover': book.cover.url,
                        'unread':book.book_leavemessage.filter(status='未读').count(),
                        'owner':book.owner.username
                            })
    return rackdic

def getbooksfromAuthor(txt):
    books = set()
    for author in Author.objects.filter(name__contains=txt):
        for book in author.author_book.all():
            books.add(book)
    return books

def getrack(request):
    data={}
    racktype=request.GET.get('racktype')
    if request.method == 'GET' : #通过ajax.GET请求渲染书架，判断当前登陆的用户的所在地，学校，渲染出本校书架，同城书架，个人书架
        if request.user.is_authenticated:
            if racktype == "city":
                city = City.objects.get(name = request.user.profile.city)
                books = city.city_book.all()
                books = getlist(books)
                data['status'] = 'online'
                data['city'] = request.user.profile.city
                data['books'] = books
                return JsonResponse(data)
            elif racktype == "school":
                school = School.objects.get(name = request.user.profile.school)
                books = school.school_book.all()
                books = getlist(books)
                data['status'] = 'online'
                data['school'] = request.user.profile.school
                data['books'] = books
                return JsonResponse(data)
            elif racktype.isdigit():
                books = User.objects.get(id=racktype).user_book.all()
                books = getlist(books)
                data['books'] = books
                return JsonResponse(data)
        else:
                books = Book.objects.filter(city=1)
                books = getlist(books)
                data['city'] = '成都'
                data['status'] = 'offline'
                data['books'] = books
                return JsonResponse(data)
    elif request.method == 'POST': #通过ajax.POST提交筛选项，直接筛选出对应的书籍进行渲染书架
        data["books"]=[]
        queryresult =[]
        txt = request.POST.get('filtertxt')
        option = request.POST.getlist('option')
        nameset = Book.objects.filter(name__contains=txt)#Book.objects.filter(name__contains='白')
        if 'author' in option and nameset:
            for book in nameset:
                    queryresult.append({'id':book.id,
                        'name': book.name ,
                        'author': book.author.name,
                        'cover': book.cover.url,
                        'unread':book.book_leavemessage.filter(status='未读').count(),
                        'owner':book.owner.username
                            })
        if 'name' in option:
            for author in Author.objects.filter(name__contains=txt):
                for book in author.author_book.all():
                    if book not in nameset:
                        queryresult.append({'id':book.id,
                            'name': book.name ,
                            'author': book.author.name,
                            'cover': book.cover.url,
                            'unread':book.book_leavemessage.filter(status='未读').count(),
                            'owner':book.owner.username
                                })
        data["books"] = queryresult
        data["status"]='filter'
        return JsonResponse(data)

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

def sendleavemessage(request):
    if(request.method=='POST'):
        content=request.POST.get('message')
        if request.POST.get('bookid'):
            id = request.POST.get('bookid')
            book = Book.objects.get(id=id)
            leaver = request.user
            try:
                message=Leavemessage(content=content,book=book,leaver=leaver,status='未读')
                message.save()
                print(message.sendtime)
                data = {
                    'message': content,
                    'leaver':leaver.username,
                    'status':'未读',
                    'sendtime':convertime(message.sendtime)
                }
            except:
                data = {
                    'status':'save error'
                }
            return JsonResponse(data)
        elif request.POST.get('userid'):
            id = request.POST.get('userid')
            owner = User.objects.get(id = id)
            leaver = request.user
            try:
                message = Userleaveboard(content=content, leaver=leaver, owner=owner, status='未读')
                message.save()
                data = {
                    'message': content,
                    'leaver': leaver.username,
                    'status': '未读',
                    'sendtime':convertime(message.sendtime)
                }
            except:
                data = {
                    'status': 'save error'
                }
            return JsonResponse(data)

def addlabel(request):
    if request.method=='POST':
        content = request.POST.get('label')
        labelfor = request.user
        try:
            label = Label(content=content,labelfor=labelfor)
            label.save()
            return JsonResponse({'status':'OK'})
        except Exception as e:
            raise e
    return JsonResponse({'status': 'ERROR'})

def getuserdata(request,id):
    if request.method=='GET':
        user = User.objects.get(id=id)
        loginuser = request.user
        reader = user.profile
        labellist=[]
        wishlist=[]
        isrequesting = 'no'
        isfriend ='no'
        isself ='no'
        if user.id ==loginuser.id:
            isself = 'yes'
        if loginuser.user_friendrequest.filter(receiver=user):
            isrequesting = 'yes'
        elif loginuser.fa_FriendShip.filter(fb=user):
            isfriend='yes'
        elif user.fa_FriendShip.filter(fb=loginuser):
            isfriend='yes'
        for label in Label.objects.filter(labelfor=id):
            labellist.append(label.content)
        for wish in user.user_wishlist.all():
            wishlist.append({'title':wish.title,'author':wish.author})
        userdata = {
            "username":user.username,
            "email":user.email,
            "city":reader.city,
            "school":reader.school,
            "grade":reader.grade,
            "labellist":labellist,
            "wishlist":wishlist,
            'isrequesting':isrequesting,
            'isfriend':isfriend,
            'isself':isself
        }
        print(userdata)
        return JsonResponse(userdata)

def getuserleaveboard(request,id):
    if request.method == 'GET':
        messagelist = []
        for m in User.objects.get(id=id).owner_userleavemessage.order_by("-sendtime"):
            messagelist.append({'leaver':m.leaver.username,'sendtime':convertime(m.sendtime),'content':m.content})

        return JsonResponse({'messagelist':messagelist})

def convertime(datetime):
    return  ('%s年%s月%s日  %s' % (
            datetime.strftime('%Y'), datetime.strftime('%m'),
            datetime.strftime('%d'), datetime.strftime('%X')))


@csrf_exempt
def addbook(request):
    if request.method =='POST':
        owner=request.user
        name = request.POST.get('title')
        author = request.POST.get('author')
        cover=request.FILES.get('cover')
        press=request.POST.get('press')
        intro = request.POST.get('intro')
        print(cover)
        if intro=="" or press=="" or name=="" or author=="":
            return JsonResponse({'status':'字段不能为空'})
        elif cover==None:
            return JsonResponse({'status': '请上传封面图'})
        else:
            if Author.objects.filter(name=author):
                nauthor = Author.objects.get(name=author)
            else :
                nauthor = Author(name=author)
                nauthor.save()
            if Press.objects.filter(name=press):
                npress = Press.objects.get(name=press)
            else:
                npress = Press(name=press)
                npress.save()
            book = Book(owner=owner,name=name,author=nauthor,
                        press=npress,
                        city=City.objects.get(name=owner.profile.city),
                        school=School.objects.get(name=owner.profile.school),
                        cover=cover,intro=intro)
            book.save()
            return JsonResponse({'status':'添加完成'})

@csrf_exempt
def addwish(request):
    if request.method=='POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        if title == "" or author == "":
            return JsonResponse({'status':'请填写书名及作者'})
        wishbook = Wishbook(owner=request.user,title=title,author=author)
        wishbook.save()
        return JsonResponse({'status':'添加完成'})

def getwishlist(request):
    wishlist = []
    if request.method=='GET':
        for n in request.user.user_wishlist.all():
            wishlist.append({'title':n.title,'author':n.author})
        return JsonResponse({'wishlist':wishlist})

@csrf_exempt
def addfriend(request):
    if request.method=='POST':
        reciveid = request.POST.get('id')
        message = request.POST.get('message')
        receiver = User.objects.get(id=reciveid)
        requester = request.user
        try:
            friendrequest = FriendRequest(requester=requester,receiver=receiver,unread=receiver,message=message)
            friendrequest.save()
            return JsonResponse({'status': '好友申请已发送'})
        except:
            return JsonResponse({'status': '数据库存入错误'})


def getmessagelist(request):
    if request.method == 'GET':
        user = request.user
        type = request.GET.get('type')
        if type == 'beensent':
            friendrequestlist = []
            exchangerequestlist = []
            for r in user.user_friendrequest.order_by("request_time"):
                time = convertime(r.request_time)
                friendrequestlist.append({'receiver':r.receiver.username,'status':r.status,'sendtime':time,'message':r.message,'type':'好友申请'})
            for e in user.user_changerequest.order_by("requesttime"):
                exchangerequestlist.append({'receiver':e.receiver.username,'booka':e.booka.name,'bookb':e.bookb.name,
                                            'message':e.message,'status':e.statusa,'sendtime':convertime(e.requesttime)})
            return JsonResponse({'friendrequestlist':friendrequestlist,'exchange_request_list':exchangerequestlist})
        elif type == 'received':
            friend_receive_list = []
            exchange_receive_list = []
            for r in user.user_friendreceive.order_by("request_time"):
                time = convertime(r.request_time)
                friend_receive_list.append(
                    {'requester': r.requester.username, 'sendtime': time, 'message': r.message})
            for e in user.user_changereceive.order_by("requesttime"):
                exchange_receive_list.append(
                    {'requester': e.requester.username, 'booka': e.booka.name, 'bookb': e.bookb.name,
                     'message': e.message,'sendtime': convertime(e.requesttime)})
            return JsonResponse({'friend_receive_list': friend_receive_list, 'exchange_receive_list': exchange_receive_list})


