from django.db import models
from masters.models import *
from questions.models import *

class ExamsCategorys(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    details = models.CharField(max_length=200, null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)
    junoocategory = models.ForeignKey(junoocategory, default=None, on_delete=models.CASCADE, null=True, blank=True)
    junoosubcategory = models.ForeignKey(junoosubcategory, default=None, on_delete=models.CASCADE, null=True,blank=True)
class quize(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    quize_id = models.CharField(max_length=200, null=True, blank=True)
    quize_time = models.CharField(max_length=200, null=True, blank=True)
    quize_tag = models.CharField(max_length=200, null=True, blank=True)
    quize_emojy = models.CharField(max_length=200, null=True, blank=True)
    quize_primary_color = models.CharField(max_length=200, null=True, blank=True)
    quize_secondary_color = models.CharField(max_length=200, null=True, blank=True)
    quize_details = models.CharField(max_length=200, null=True, blank=True)

    quize_cutoffmark = models.CharField(max_length=200, null=True, blank=True)

    #zero free
    win_price = models.CharField(max_length=200, null=True, blank=True)
    entry_fee = models.CharField(max_length=200, null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)
    junoocategory = models.ForeignKey(junoocategory, default=None, on_delete=models.CASCADE, null=True, blank=True)
    junoosubcategory = models.ForeignKey(junoosubcategory, default=None, on_delete=models.CASCADE, null=True,blank=True)
    def __str__(self):
        return self.title
    @property
    def get_quize_questions(self):
        return quize_questions.objects.filter(quize=self.id)
class quize_questions(models.Model):
    quize = models.ForeignKey(quize, default=None, on_delete=models.CASCADE, null=True, blank=True)
    questions = models.ForeignKey(questions, default=None, on_delete=models.CASCADE, null=True, blank=True)



