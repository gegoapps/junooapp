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
    isBlocked = models.BooleanField(default=False, null=True, blank=True)
    blockedReason = models.CharField(max_length=200, null=True, blank=True)
    current_totalpoint = models.CharField(max_length=200, null=True, blank=True,default=0)
    country_code = models.CharField(max_length=200, null=True, blank=True)
    img = models.ImageField(upload_to='customers', null=True, blank=True)
    junoocategory = models.ForeignKey(junoocategory, on_delete=models.CASCADE, default=None,  null=True, blank=True)
    junoosubcategory = models.ForeignKey(junoosubcategory, on_delete=models.CASCADE, default=None, null=True, blank=True)
class PointHistory(models.Model):
    customer = models.ForeignKey(Customer, default=None, on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=False)
    created_point = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    #true is for positive
    status = models.BooleanField(default=False, null=True, blank=True)
    # used True
    used_or_get = models.BooleanField(default=False, null=True, blank=True)

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
    is_passed = models.CharField(max_length=200, null=True, blank=True)
    earnedpoint = models.CharField(max_length=200, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=False)
    created_time = models.TimeField(max_length=200, null=True, blank=True)

    @property
    def get_Quize_attended_questions(self):
        return Quize_attended_questions.objects.filter(quizehistory=self.id)

class Quize_attended_questions(models.Model):
    quize = models.ForeignKey(quize, default=None, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, default=None, on_delete=models.CASCADE, null=True, blank=True)
    quize_attended_code = models.CharField(max_length=200, null=True, blank=True)
    quizehistory = models.ForeignKey(QuizeHistory, default=None, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(questions, default=None, on_delete=models.CASCADE, null=True, blank=True)
    right_wrong = models.BooleanField(default=False, null=True, blank=True)
    crt_option = models.CharField(max_length=200, null=True, blank=True)
    selected_ans = models.CharField(max_length=200, null=True, blank=True)





class ExamHistory(models.Model):
    ExamList = models.ForeignKey(ExamList, default=None, on_delete=models.CASCADE, null=True, blank=True)
    exam_attended_code=models.CharField(max_length=200, null=True, blank=True)
    customer = models.ForeignKey(Customer, default=None, on_delete=models.CASCADE, null=True, blank=True)
    total_questions=models.CharField(max_length=200, null=True, blank=True)
    total_right_answers=models.CharField(max_length=200, null=True, blank=True)
    total_wrong_answer = models.CharField(max_length=200, null=True, blank=True)
    total_mark = models.CharField(max_length=200, null=True, blank=True)
    is_passed = models.CharField(max_length=200, null=True, blank=True)
    earnedpoint = models.CharField(max_length=200, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=False)
    created_time = models.TimeField(max_length=200, null=True, blank=True)

    @property
    def get_Exam_attended_questions(self):
        return Exam_attended_questions.objects.filter(ExamHistory=self.id)
class Exam_attended_questions(models.Model):
    ExamList = models.ForeignKey(ExamList, default=None, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, default=None, on_delete=models.CASCADE, null=True, blank=True)
    exam_attended_code = models.CharField(max_length=200, null=True, blank=True)
    ExamHistory = models.ForeignKey(ExamHistory, default=None, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(questions, default=None, on_delete=models.CASCADE, null=True, blank=True)
    right_wrong = models.BooleanField(default=False, null=True, blank=True)
    crt_option = models.CharField(max_length=200, null=True, blank=True)
    selected_ans = models.CharField(max_length=200, null=True, blank=True)





class SPExamHistory(models.Model):
    specialExam = models.ForeignKey(specialExam, default=None, on_delete=models.CASCADE, null=True, blank=True)
    exam_attended_code=models.CharField(max_length=200, null=True, blank=True)
    customer = models.ForeignKey(Customer, default=None, on_delete=models.CASCADE, null=True, blank=True)
    total_questions=models.CharField(max_length=200, null=True, blank=True)
    total_right_answers=models.CharField(max_length=200, null=True, blank=True)
    total_wrong_answer = models.CharField(max_length=200, null=True, blank=True)
    total_mark = models.CharField(max_length=200, null=True, blank=True)
    attended_time = models.CharField(max_length=200, null=True, blank=True)
    iscutoffpassed = models.BooleanField(default=False, null=True, blank=True)
    point_claimed = models.BooleanField(default=False, null=True, blank=True)
    is_passed = models.CharField(max_length=200, null=True, blank=True)
    earnedpoint = models.CharField(max_length=200, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=False)
    created_time = models.TimeField(max_length=200, null=True, blank=True)

    @property
    def get_SPExam_attended_questions(self):
        return SPExam_attended_questions.objects.filter(SPExamHistory=self.id)


class SPExam_attended_questions(models.Model):
    specialExam = models.ForeignKey(specialExam, default=None, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, default=None, on_delete=models.CASCADE, null=True, blank=True)
    exam_attended_code = models.CharField(max_length=200, null=True, blank=True)
    SPExamHistory = models.ForeignKey(SPExamHistory, default=None, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(questions, default=None, on_delete=models.CASCADE, null=True, blank=True)
    right_wrong = models.BooleanField(default=False, null=True, blank=True)
    crt_option = models.CharField(max_length=200, null=True, blank=True)
    selected_ans = models.CharField(max_length=200, null=True, blank=True)

