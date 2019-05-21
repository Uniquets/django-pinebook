from django.conf import settings as original_settings
from friend.models import *
from pineBook.forms import loginForm

def initdata(request):
    form = loginForm()
    if request.user.is_authenticated:
        friends = []
        for n in FriendShip.objects.filter(fa=request.user.id):
            friends.append({'id': n.fb, 'name': User.objects.get(id=n.fb).username})
        for n in FriendShip.objects.filter(fb=request.user.id):
            friends.append({'id': n.fb, 'name': User.objects.get(id=n.fa).username})
        return {'username': request.user.username, 'friends': friends,'loginform': form}
    return {'loginform': form}
