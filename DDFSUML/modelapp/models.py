from django.db import models
import uuid
from django.contrib.auth.models import User
import indian_names
# Create your models here.



class Symp(models.Model):
  name=models.CharField(max_length=200)
  created = models.DateTimeField(auto_now_add=True)


  def __str__(self):
    return self.name

class DiseaseDesc(models.Model):
  name = models.CharField(max_length=200)
  desc = models.TextField()

  def __str__(self):
    return self.name

class About(models.Model):
  name = models.CharField(max_length=200)
  position = models.CharField(max_length=200)
  description = models.TextField()
  imglink = models.URLField()

  def __str__(self):
    return self.name

class Profile(models.Model):
  user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
  name=models.CharField(max_length=200 ,null=True,blank=True)
  email=models.EmailField(max_length=500,null=True,blank=True)
  username  = models.CharField(max_length=200 ,null=True,blank=True)
  location  = models.CharField(max_length=200 ,null=True,blank=True)
  education=models.CharField(max_length=200 ,null=True,blank=True)
  bio=models.TextField(null=True,blank=True)
  website=models.CharField(max_length=200 ,null=True,blank=True)
  created = models.DateTimeField(auto_now_add=True)
  id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

  def __str__(self):
    return str(self.username)


class queryToDoc(models.Model):
  nickname = models.CharField(max_length=555,default='John Doe')
  listosymp = models.CharField(max_length=999 ,null=True,blank=True)
  predDiseases = models.CharField(max_length=999 ,null=True,blank=True)
  note = models.TextField()
  created = models.DateTimeField(auto_now_add=True)
  mail = models.EmailField(null=False)
  id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
  complete= models.BooleanField(default=False)
  doc = models.CharField(max_length=999 ,null=False,blank=False,default="None")
  docnote = models.TextField(blank=True)
  probsolve = models.DateTimeField(blank=True,auto_now_add=True)



  def __str__(self):
    return str(self.nickname)