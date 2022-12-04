from django.db import models
from django.contrib.auth.models import User
from masters.models import *
from questions.models import *
from quizes.models import *
# Create your models here.
from rest_framework import serializers

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True, blank=False)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)
    current_totalpoint = models.CharField(max_length=200, null=True, blank=True,default=0)
    country_code = models.CharField(max_length=200, null=True, blank=True)
    junoocategory = models.ForeignKey(junoocategory, on_delete=models.CASCADE, default=None,  null=True, blank=True)
    junoosubcategory = models.ForeignKey(junoosubcategory, on_delete=models.CASCADE, default=None, null=True, blank=True)
class PointHistory(models.Model):
    customer = models.ForeignKey(Customer, default=None, on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=False)
    created_point = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    #true is for positive
    status = models.BooleanField(default=False, null=True, blank=True)

class CustomerFcm(models.Model):
    customer = models.ForeignKey(Customer, default=None, on_delete=models.CASCADE, null=True, blank=True)
    fcm_key= models.CharField(max_length=200, null=True, blank=True)
    created_date=models.DateField(auto_now_add=True, null=True, blank=False)


class qanda_attended_log(models.Model):
    customer = models.ForeignKey(Customer, default=None, on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=False)
    right_answr = models.CharField(max_length=200, null=True, blank=True)
    wrong_answr = models.CharField(max_length=200, null=True, blank=True)
    skiped_answr = models.CharField(max_length=200, null=True, blank=True)

class QuizeHistory(models.Model):
    quize = models.ForeignKey(quize, default=None, on_delete=models.CASCADE, null=True, blank=True)
    quize_attended_code=models.CharField(max_length=200, null=True, blank=True)
    customer = models.ForeignKey(Customer, default=None, on_delete=models.CASCADE, null=True, blank=True)
    total_questions=models.CharField(max_length=200, null=True, blank=True)
    total_right_answers=models.CharField(max_length=200, null=True, blank=True)
    total_wrong_answer = models.CharField(max_length=200, null=True, blank=True)

class Quize_attended_questions(models.Model):
    quize = models.ForeignKey(quize, default=None, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, default=None, on_delete=models.CASCADE, null=True, blank=True)
    quize_attended_code = models.CharField(max_length=200, null=True, blank=True)
    quizehistory = models.ForeignKey(QuizeHistory, default=None, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(questions, default=None, on_delete=models.CASCADE, null=True, blank=True)
    right_wrong = models.BooleanField(default=False, null=True, blank=True)
    crt_option = models.CharField(max_length=200, null=True, blank=True)

