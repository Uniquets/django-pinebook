
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
    url(r'^showbook/$',views.showbook,name = "showbook"),
    url(r'^logout/$', views.logout,name="logout"),
    url(r'^register/$',views.register,name="register"),
    url(r'^personal/$',views.personal,name='personal'),
    url(r'^register/sendemail/$',views.sendemail,name='register_sendemail'),
    url(r'^searchuser/$',views.searchuser,name='searchuser')
]
