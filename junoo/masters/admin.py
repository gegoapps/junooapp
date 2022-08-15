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
    list_display = ('name','mobile','country_code','date','junoocategory','junoosubcategory')
    list_filter = ('mobile','status')
admin.site.register(Customer,AddClassesCustomer)

class AddClassesdoyouknow(admin.ModelAdmin):
    # exclude = ('is_deleted',)
    list_display = ('title','status','photo_tag')
    list_filter = ('title',)

    def photo_tag(self,obj):
        return format_html(f'<img src="/media/{obj.img}" style="height:100px;width:100px" />')

admin.site.register(doyouknow,AddClassesdoyouknow)
