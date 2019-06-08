from django.contrib import admin
import users.models as user
from friend.models import *


admin.site.register(user.School)
admin.site.register(user.Reader)
admin.site.register(user.City)
admin.site.register(user.Userleaveboard)
admin.site.register(user.Label)
admin.site.register(Book)
admin.site.register(Press)
admin.site.register(Author)
admin.site.register(Leavemessage)
admin.site.register(Changerequest)
admin.site.register(Wishbook)
admin.site.register(FriendRequest)
admin.site.register(FriendShip)

