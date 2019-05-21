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

class Reader(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="profile",null=False)
    #扩展User，on_delete删除关联数据,与之关联也删除，related_name自定义外键名
    sex = models.CharField(max_length=5,null=False)
    telephone = models.CharField(max_length=11,null=False)
    city = models.CharField(max_length=30,null=False)
    school = models.CharField(max_length=80,null=False)
    grade = models.CharField(max_length=20,null=False,default="2015")

    class Meta:   #Meta详解   https://www.cnblogs.com/flash55/p/6265405.html
        verbose_name = '读者'

    def __str__(self):
        return self.user.__str__()


class City(models.Model):
    name = models.CharField(max_length=30, null=False)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class School(models.Model):
    name = models.CharField(max_length=30, null=False)
    location = models.ForeignKey(City, on_delete=models.SET_DEFAULT, default=1)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name