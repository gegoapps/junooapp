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