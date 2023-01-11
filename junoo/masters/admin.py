from django.contrib import admin
from.models import *
from appapi.models import *
from django.utils.html import format_html
class AddClassesjunoocategory(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('title','status',)
    list_filter = ('title',)
admin.site.register(junoocategory,AddClassesjunoocategory)


class AddClassesjunoosubcategory(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('junoocategory','title','status',)
    list_filter = ('title',)
admin.site.register(junoosubcategory,AddClassesjunoosubcategory)

class AddClassesCustomer(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('img','name','mobile','country_code','date','junoocategory','junoosubcategory','current_totalpoint')
    list_filter = ('mobile','status')
admin.site.register(Customer,AddClassesCustomer)

class AddClassesPointHistory(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('customer','created_date','created_point','title','status')
    list_filter = ('customer','status')
admin.site.register(PointHistory,AddClassesPointHistory)

class AddClassesdoyouknow(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('title','status','photo_tag')
    list_filter = ('title',)

    def photo_tag(self,obj):
        return format_html(f'<img src="/media/{obj.img}" style="height:100px;width:100px" />')

admin.site.register(doyouknow,AddClassesdoyouknow)


class AddClassesappopen_data(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('title','details')
    list_filter = ('title',)

admin.site.register(appopen_data,AddClassesappopen_data)

class AddClassesslider(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('junoocategory','junoosubcategory','status','photo_tag','screen','title','appscreen_id')
    list_filter = ('status',)

    def photo_tag(self,obj):
        return format_html(f'<img src="/media/{obj.img}" style="height:100px;width:100px" />')

admin.site.register(slider,AddClassesslider)

class Addqanda_attended_log(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('customer','created_date','right_answr','wrong_answr','skiped_answr')

admin.site.register(qanda_attended_log,Addqanda_attended_log)


class AddQuizeHistory(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('quize','created_date','quize_attended_code','customer','total_questions','total_right_answers','total_wrong_answer')


admin.site.register(QuizeHistory,AddQuizeHistory)


class AddQuize_attended_questions(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('quize','quize_attended_code','customer','quizehistory','question','right_wrong','crt_option','selected_ans')

admin.site.register(Quize_attended_questions,AddQuize_attended_questions)




class AddExamHistory(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('created_time','created_date','ExamList','exam_attended_code','customer','total_questions','total_right_answers','total_wrong_answer','total_mark')


admin.site.register(ExamHistory,AddExamHistory)


class AddExam_attended_questions(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('ExamList','exam_attended_code','customer','ExamHistory','question','right_wrong','crt_option','selected_ans')

admin.site.register(Exam_attended_questions,AddExam_attended_questions)

