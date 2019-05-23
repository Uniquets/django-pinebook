from django.conf import settings as original_settings
from friend.models import *
from pineBook.forms import loginForm

def initdata(request):
    form = loginForm()
    if request.user.is_authenticated:
        database = getdatalist()
        friends = getfriendslist(request.user.id)
        userdata = getuserdata(request.user.id)
        return {'username': request.user.username,
                'friends': friends,
                'loginform': form,
                'userdata':userdata,
                'database':database
                }
    return {'loginform': form}

def getdatalist():
    database={}
    citylist = []
    for city in City.objects.all():
        citylist.append(city.name)
    schoollist = []
    for school in School.objects.all():
        schoollist.append(school.name)
    labellist = set()
    for label in Label.objects.all()[0:10]:
        labellist.add(label.content)
    labellist = list(labellist)
    database={
        'citylist':citylist,
        'schoollist':schoollist,
        'labellist':labellist
    }
    return database


def getfriendslist(userid):
    friends = []
    for n in FriendShip.objects.filter(fa=userid):
        friends.append({'id': n.fb, 'name': User.objects.get(id=n.fb).username})
    for n in FriendShip.objects.filter(fb=userid):
        friends.append({'id': n.fb, 'name': User.objects.get(id=n.fa).username})
    return friends

def getuserdata(userid):
    user = User.objects.get(id=userid)
    reader = user.profile
    labellist=[]
    for label in Label.objects.filter(labelfor=userid):
        labellist.append(label.content)
    userdata = {
        "用户名":user.username,
        "邮箱地址":user.email,
        "性别":reader.sex,
        "城市":reader.city,
        "学校":reader.school,
        "是否在校":reader.grade,
        "个人标签":labellist
    }
    return userdata


