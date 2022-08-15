from django.db import models
from masters.models import *
class subject(models.Model):
    junoocategory = models.ForeignKey(junoocategory, default=None, on_delete=models.CASCADE, null=True, blank=True)
    junoosubcategory = models.ForeignKey(junoosubcategory, default=None, on_delete=models.CASCADE, null=True,
                                         blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)
    def __str__(self):
        return self.title
    @property
    def get_chapters(self):
        return chapter.objects.filter(subject=self.id)

class chapter(models.Model):
    subject = models.ForeignKey(subject, default=None, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)
    def __str__(self):
        return self.title
class questions(models.Model):
    junoocategory = models.ForeignKey(junoocategory, default=None, on_delete=models.CASCADE, null=True, blank=True)
    junoosubcategory = models.ForeignKey(junoosubcategory, default=None, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(subject, default=None, on_delete=models.CASCADE, null=True, blank=True)
    chapter = models.ForeignKey(chapter, default=None, on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.CharField(max_length=200, null=True, blank=True)
    #true active
    status = models.BooleanField(default=False, null=True, blank=True)
    #true verified
    verification = models.BooleanField(default=False, null=True, blank=True)
    title = models.CharField(max_length=900, null=True, blank=True)
    option1 = models.CharField(max_length=900, null=True, blank=True)
    option2 = models.CharField(max_length=900, null=True, blank=True)
    option3 = models.CharField(max_length=900, null=True, blank=True)
    option4 = models.CharField(max_length=900, null=True, blank=True)
    answer = models.CharField(max_length=900, null=True, blank=True)
    current_affairs = models.BooleanField(default=False, null=True, blank=True)
    current_affairs_date = models.CharField(max_length=900, null=True, blank=True)
    def __str__(self):
        return self.title


