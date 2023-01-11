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



class ExamList(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    el_id = models.CharField(max_length=200, null=True, blank=True)
    el_time = models.CharField(max_length=200, null=True, blank=True)
    el_tag = models.CharField(max_length=200, null=True, blank=True)
    el_emojy = models.CharField(max_length=200, null=True, blank=True)
    el_primary_color = models.CharField(max_length=200, null=True, blank=True)
    el_secondary_color = models.CharField(max_length=200, null=True, blank=True)
    el_details = models.CharField(max_length=200, null=True, blank=True)
    el_positivemark = models.CharField(max_length=200, null=True, blank=True)
    negativemark = models.CharField(max_length=200, null=True, blank=True)
    el_cutoffmark = models.CharField(max_length=200, null=True, blank=True)

    #zero free
    win_price = models.CharField(max_length=200, null=True, blank=True)
    entry_fee = models.CharField(max_length=200, null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)
    pre_or_moc = models.BooleanField(default=False, null=True, blank=True)
    ExamCategorys = models.ForeignKey(ExamsCategorys, default=None, on_delete=models.CASCADE, null=True, blank=True)
    junoocategory = models.ForeignKey(junoocategory, default=None, on_delete=models.CASCADE, null=True, blank=True)
    junoosubcategory = models.ForeignKey(junoosubcategory, default=None, on_delete=models.CASCADE, null=True,blank=True)
    def __str__(self):
        return self.title
    @property
    def get_quize_questions(self):
        return exam_questions.objects.filter(quize=self.id)
class exam_questions(models.Model):
    ExamList = models.ForeignKey(ExamList, default=None, on_delete=models.CASCADE, null=True, blank=True)
    questions = models.ForeignKey(questions, default=None, on_delete=models.CASCADE, null=True, blank=True)



class specialExam(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    el_id = models.CharField(max_length=200, null=True, blank=True)
    el_time = models.CharField(max_length=200, null=True, blank=True)
    el_tag = models.CharField(max_length=200, null=True, blank=True)
    el_emojy = models.CharField(max_length=200, null=True, blank=True)
    el_primary_color = models.CharField(max_length=200, null=True, blank=True)
    el_secondary_color = models.CharField(max_length=200, null=True, blank=True)
    el_details = models.CharField(max_length=200, null=True, blank=True)
    el_positivemark = models.CharField(max_length=200, null=True, blank=True)
    negativemark = models.CharField(max_length=200, null=True, blank=True)
    el_cutoffmark = models.CharField(max_length=200, null=True, blank=True)
    published = models.BooleanField(default=False, null=True, blank=True)
    result_published = models.BooleanField(default=False, null=True, blank=True)

    opportunity_to_get_mark = models.CharField(max_length=200, null=True, blank=True)
    publishtime = models.CharField(max_length=200, null=True, blank=True)
    #zero free
    win_price = models.CharField(max_length=200, null=True, blank=True)
    entry_fee = models.CharField(max_length=200, null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)

    junoocategory = models.ForeignKey(junoocategory, default=None, on_delete=models.CASCADE, null=True, blank=True)
    junoosubcategory = models.ForeignKey(junoosubcategory, default=None, on_delete=models.CASCADE, null=True,blank=True)
    def __str__(self):
        return self.title
    @property
    def get_spexam_questions(self):
        return spexam_questions.objects.filter(quize=self.id)
class spexam_questions(models.Model):
    specialExam = models.ForeignKey(specialExam, default=None, on_delete=models.CASCADE, null=True, blank=True)
    questions = models.ForeignKey(questions, default=None, on_delete=models.CASCADE, null=True, blank=True)





