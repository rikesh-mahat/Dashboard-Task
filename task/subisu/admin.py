from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib import admin
<<<<<<< HEAD
=======


# from import_export.admin import ImportExportModelAdmin


>>>>>>> 6a293eabeff09b43f036af443e50eafde04b8e83

# services ra host lai register gareko
class ServiceInline(admin.StackedInline):
    model = Service
    extra = 0

# client table lai register gareko
class HostClientContact(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'email', 'status', 'registerDate')
    
admin.site.register(ClientContact, HostClientContact)

class ActivityInline(admin.StackedInline):
    readonly_fields = ('actId','comment', 'commentBy', 'timeStamp')
    model = ActivitiesComment
    extra = 0


class POAInline(admin.StackedInline):
    model = Poa
    extra = 0
    
class HostActivities(admin.ModelAdmin):
    list_display = ('id', 'title', 'ETA','startTime', 'endTime', 'created')
    inlines = [ActivityInline, POAInline]
    list_filter = ('title','created')
    search_fields = ('id', 'title')
    
admin.site.register(Activities, HostActivities)


# class HostPOA(admin.ModelAdmin):
#     list_display = ('id', 'activityId', 'Engineers','poaDetails', 'poaEntry')
    
#     def Engineers(self, obj):
#         return ', '.join([x.firstName for x in obj.fieldEngineer.all()])
    
# admin.site.register(Poa,HostPOA)


class HostEmailNotification(admin.ModelAdmin):
    list_display = ['activityId', 'emailBody', 'logTime']
    list_filter = ('activityId', 'logTime')
    
admin.site.register(EmailNotification, HostEmailNotification)


