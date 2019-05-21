from django.db import models
from users.models import *
import uuid


class Press(models.Model):
    name = models.CharField(max_length=30,null=False)
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50,null=False)
    country = models.CharField(max_length=30,default="中国")
    def __str__(self):
        return self.name


def custom_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return filename

class Book(models.Model):
    owner = models.ForeignKey(Reader,on_delete=models.CASCADE,related_name="reader_book",null=False,default=2)
    name = models.CharField(max_length=30,null=False)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name="author_book",null=False)
    press = models.ForeignKey(Press,on_delete=models.CASCADE,related_name="press_book",null=False)
    city = models.ForeignKey(City,on_delete=models.CASCADE,related_name="city_book",null=False)
    school = models.ForeignKey(School,on_delete=models.CASCADE,related_name="school_book",null=False)
    cover = models.ImageField(upload_to=custom_path,blank=True)
    intro = models.CharField(max_length=100)
    def __str__(self):
        return self.name

    def toJSON(self):
        import json
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.__str__ for f in self._meta.fields]]))








