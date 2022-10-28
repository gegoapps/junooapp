from django.db import models
from django.contrib.auth.models import User
from masters.models import *
# Create your models here.
from rest_framework import serializers

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,db_constraint=False)
    date = models.DateField(auto_now_add=True, null=True, blank=False)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)
    country_code = models.CharField(max_length=200, null=True, blank=True)
    junoocategory = models.ForeignKey(junoocategory, on_delete=models.CASCADE, default=None,  null=True, blank=True)
    junoosubcategory = models.ForeignKey(junoosubcategory, on_delete=models.CASCADE, default=None, null=True, blank=True)

class CustomerFcm(models.Model):
    customer = models.ForeignKey(Customer, default=None, on_delete=models.CASCADE, null=True, blank=True)
    fcm_key= models.CharField(max_length=200, null=True, blank=True)
    created_date=models.DateField(auto_now_add=True, null=True, blank=False)