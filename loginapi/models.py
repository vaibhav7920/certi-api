from django.db import models
from django import forms
# Create your models here.
class Userverification(models.Model):
    name=models.CharField(max_length=200,blank=False)
    email=models.CharField(max_length=200,blank=False)