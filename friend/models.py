from django.db import models
from book.models import *

class FriendShip(models.Model):
    fa = models.ForeignKey(User,on_delete=models.CASCADE,related_name='fa_FriendShip',verbose_name="用户A")
    fb = models.ForeignKey(User,on_delete=models.CASCADE,related_name='fb_FriendShip',verbose_name="用户B")

class FriendRequest(models.Model):
    requester = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_friendrequest',default=None,verbose_name="发起人")
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_friendreceive',default=None,verbose_name="接收人")
    status = models.CharField(max_length=10,default='已申请',verbose_name="状态")
    unread = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_unreadfriendrequest',default=None,verbose_name="未读方")
    request_time = models.DateTimeField(auto_now=True,verbose_name="发起时间")
    message = models.CharField(max_length=50,default="",verbose_name="附加信息")
