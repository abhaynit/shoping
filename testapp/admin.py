from django.contrib import admin
#from django.contrib.auth import models
from .models import items,carted1,ordered,addressed,addimg,mov_ticket,cinema_hall,select_halls
# Register your models here.
@admin.register(items)
class itemAdmin(admin.ModelAdmin):
    list_display = ['id','iname','itype','price','pic']

@admin.register(carted1)
class carted1Admin(admin.ModelAdmin):
    list_display = ['id','user','sel']

@admin.register(ordered)
class orderedAdmin(admin.ModelAdmin):
    list_display = ['id','user','ite','status']

@admin.register(addressed)
class addressAdmin(admin.ModelAdmin):
    list_display = ['id','user','city','state','zip_code','street','mobile']

   

@admin.register(addimg)
class addimg(admin.ModelAdmin):
    list_display=['user','im']

@admin.register(mov_ticket)
class mo_ticket(admin.ModelAdmin):
    list_display = ['mname','image','orig','disp','utm']



@admin.register(cinema_hall)
class cinema(admin.ModelAdmin):
    list_display = ['hname','city','state','street','pin','contact']



@admin.register(select_halls)
class hall_select(admin.ModelAdmin):
    list_display = ['movie','hall','seat']

