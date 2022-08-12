from django.contrib import admin
from.models import *


class AddClassessubject(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('title','status',)
    list_filter = ('title',)
admin.site.register(subject,AddClassessubject)

class AddClassesschapter(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('title','subject','status',)
    list_filter = ('title',)
admin.site.register(chapter,AddClassesschapter)


class AddClassesquestions(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('title','option1','option2','option3','option4','answer','junoocategory','junoosubcategory','subject','chapter','created_date','verification',)
    list_filter = ('status','title')
admin.site.register(questions,AddClassesquestions)