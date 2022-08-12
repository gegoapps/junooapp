from django.contrib import admin
from.models import *
class AddClassesStaff(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('username','password','name','phone','date',)
    list_filter = ('phone','status')
admin.site.register(Staff,AddClassesStaff)

