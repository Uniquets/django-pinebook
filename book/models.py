from django.db import models
from users.models import *
import uuid


class Press(models.Model):
    name = models.CharField(max_length=30,null=False,verbose_name="名称")
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50,null=False,verbose_name="作者名称")
    country = models.CharField(max_length=30,default="中国",verbose_name="国籍")
    def __str__(self):
        return self.name


def custom_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return filename

class Book(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_book",null=False,default=2,verbose_name="持有人")
    name = models.CharField(max_length=30,null=False,verbose_name="书名")
    author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name="author_book",null=False,verbose_name="作者")
    press = models.ForeignKey(Press,on_delete=models.CASCADE,related_name="press_book",null=False,verbose_name="出版社")
    city = models.ForeignKey(City,on_delete=models.CASCADE,related_name="city_book",null=False,verbose_name="所在城市")
    school = models.ForeignKey(School,on_delete=models.CASCADE,related_name="school_book",null=False,verbose_name="所在学校")
    cover = models.ImageField(upload_to=custom_path,blank=True,verbose_name="封面图")
    intro = models.CharField(max_length=100,verbose_name="简介")
    def __str__(self):
        return self.name

class Leavemessage(models.Model):
    content = models.CharField(max_length=200,null=False,verbose_name="留言内容")
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='book_leavemessage',default=None,verbose_name="关联书籍")
    leaver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='leaver_leavemessage',default=None,verbose_name="留言者")
    sendtime = models.DateTimeField(auto_now=True,verbose_name="发送时间")
    status = models.CharField(max_length=10,null=False,default='未读',verbose_name="状态")
    def __str__(self):
        return self.content


class Changerequest(models.Model):
    requesttime = models.DateTimeField(auto_now=True,verbose_name="申请时间")
    requester = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_changerequest',default=None,verbose_name="发送者")
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_changereceive',default=None,verbose_name="接收者")
    booka = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='book_asbooka',default=None,verbose_name="被请求的书籍")
    bookb = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='book_asbookb',default=None,verbose_name="用于交换的书籍")
    unread = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_unreadchangerequest',default=None,verbose_name="未读方")
    message = models.CharField(max_length=30,verbose_name="附加信息")
    statusa = models.CharField(max_length=10,default='已申请',verbose_name="发送者处理状态")
    statusb = models.CharField(max_length=10,default='已申请',verbose_name="接收者处理状态")
    def __str__(self):
        return self.requester.name


class Wishbook(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_wishlist',verbose_name="拥有者")
    title = models.CharField(max_length=30,verbose_name="书标题")
    author = models.CharField(max_length=30,verbose_name="作者")
    def __str__(self):
        return self.title








