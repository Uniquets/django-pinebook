from django.db import models
from book.models import *

class FriendShip(models.Model):
    fa = models.CharField(max_length=10)
    fb = models.CharField(max_length=10)

class FriendRequest(models.Model):
    propser = models.ForeignKey(Reader,on_delete=models.CASCADE,related_name='reader_friendrequest')
    receiver = models.ForeignKey(Reader,on_delete=models.CASCADE,related_name='reader_friendreceive')
    status = models.CharField(max_length=10)
    request_time = models.DateTimeField(auto_now=True)
    deal_time = models.DateTimeField()
    message = models.CharField(max_length=50)
