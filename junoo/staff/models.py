from django.db import models
from django.contrib.auth.models import User
from masters.models import *

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True, blank=False)
    username = models.CharField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)
