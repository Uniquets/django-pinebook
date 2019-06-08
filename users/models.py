from django.db import models
from django.contrib.auth.models import User

#on_delete=None,               # 删除关联表中的数据时,当前表与其关联的field的行为
#on_delete=models.CASCADE,     # 删除关联数据,与之关联也删除
#on_delete= DO_NOTHING_         # 删除关联数据,什么也不做
#on_delete=models.PROTECT,     # 删除关联数据,引发错误ProtectedError
# models.ForeignKey('关联表', on_delete=models.SET_NULL, blank=True, null=True)
#on_delete=models.SET_NULL,    # 删除关联数据,与之关联的值设置为null（前提FK字段需要设置为可空,一对一同理）
# models.ForeignKey('关联表', on_delete=models.SET_DEFAULT, default='默认值')
#on_delete=models.SET_DEFAULT, # 删除关联数据,与之关联的值设置为默认值（前提FK字段需要设置默认值,一对一同理）
#on_delete=models.SET,         # 删除关联数据

class Label(models.Model):
    labelfor = models.ForeignKey(User,on_delete=models.CASCADE, related_name="user_labels",default=1,verbose_name="关联用户")
    content = models.CharField(max_length=12,null=False,verbose_name="内容")

class Reader(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="profile",null=False,verbose_name="关联用户")
    #扩展User，on_delete删除关联数据,与之关联也删除，related_name自定义外键名
    sex = models.CharField(max_length=5,verbose_name="性别")
    telephone = models.CharField(max_length=11,null=False,verbose_name="电话号码")
    city = models.CharField(max_length=30,null=False,verbose_name="城市")
    school = models.CharField(max_length=80,null=False,verbose_name="学校")
    grade = models.CharField(max_length=20,default="2015",verbose_name="年级")
    class Meta:   #Meta详解   https://www.cnblogs.com/flash55/p/6265405.html
        verbose_name = '读者'

    def __str__(self):
        return self.user.__str__()

class Userleaveboard(models.Model):
    content = models.CharField(max_length=200,null=False,verbose_name="留言内容")
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='owner_userleavemessage',verbose_name="留言者")
    leaver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='leaver_userleavemessage',verbose_name="留言板主人")
    sendtime = models.DateTimeField(auto_now=True,verbose_name="发送时间")
    status = models.CharField(max_length=10,null=False,default='未读',verbose_name="状态")


class City(models.Model):
    name = models.CharField(max_length=30, null=False,verbose_name="城市名称")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class School(models.Model):
    name = models.CharField(max_length=30, null=False,verbose_name="学校名称")
    location = models.ForeignKey(City, on_delete=models.SET_DEFAULT, default=1,verbose_name="哪座城市")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name