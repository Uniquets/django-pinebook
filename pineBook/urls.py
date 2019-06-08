
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from . import views
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/imag/icon.jpg', permanent=True)
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^favicon\.ico$', favicon_view),
    url(r'^$', views.homepage,name="index"),
    url(r'^getrack/$',views.getrack,name = "getrack"),
    url(r'^logout/$', views.logout,name="logout"),
    url(r'^register/$',views.register,name="register"),
    url(r'^personal/$',views.personal,name='personal'),
    url(r'^register/sendemail/$',views.sendemail,name='register_sendemail'),
    url(r'^searchuser/$',views.searchuser,name='searchuser'),
    url(r'^booklayer/(?P<id>\d+)/$',views.booklayer,name='booklayer'),
    url(r'^sendleavemessage/$',views.sendleavemessage,name='sendleavemessage'),
    url(r'^sendchangerequest/$',views.sendchangerequest,name='sendchangerequest'),
    url(r'^addlabel/$',views.addlabel,name='addlabel'),
    url(r'^getuserdata/(?P<id>\d+)/$',views.getuserdata,name='getuserdata'),
    url(r'^getuserleaveboard/(?P<id>\d+)/$',views.getuserleaveboard,name='getuserleaveboard'),
    url(r'^addbook/$',views.addbook,name='addbook'),
    url(r'^addwish/$',views.addwish,name='addwish'),
    url(r'^getwishlist/$',views.getwishlist,name='getwishlist'),
    url(r'^addfriend/$',views.addfriend,name='addfriend'),
    url(r'^getmessagelist/$',views.getmessagelist,name='getmessagelist')
]
