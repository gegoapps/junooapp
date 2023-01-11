from django.contrib import admin
from.models import *


class AddClassesquize(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('title','status','quize_id','entry_fee',)
    list_filter = ('title',)
admin.site.register(quize,AddClassesquize)

class AddClassesquize_questions(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('questions','quize',)
admin.site.register(quize_questions,AddClassesquize_questions)


class AddClassesExamsCategorys(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('title','status','details','junoocategory','junoosubcategory')
admin.site.register(ExamsCategorys,AddClassesExamsCategorys)



class AddClassesExamList(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('title','status','el_time','win_price','negativemark','junoocategory','junoosubcategory')
admin.site.register(ExamList,AddClassesExamList)



class Addexam_questions(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('questions','ExamList',)
admin.site.register(exam_questions,Addexam_questions)

class AddClassesspecialExam(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('title','status','el_time','win_price','negativemark','junoocategory','junoosubcategory')
admin.site.register(specialExam,AddClassesspecialExam)


class AddClassesspexam_questions(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('questions','specialExam',)
admin.site.register(spexam_questions,AddClassesspexam_questions)