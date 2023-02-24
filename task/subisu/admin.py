from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register([ServiceType])

# services ra host lai register gareko
class ServiceInline(admin.StackedInline):
    model = Service
    extra = 0

class HostAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'ip', 'dcID','services')
    inlines = [ServiceInline]
    
    def services(self, obj):
        return ', '.join([s.srvType.serviceName for s in obj.services.all()])
    
    services.short_description = 'Services'
    
admin.site.register(Host, HostAdmin)

# datacenter table lai register gareko
class HostDataCenter(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact')
    
    
admin.site.register(Datacenter, HostDataCenter)

# client table lai register gareko
class HostClientContact(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'email', 'status', 'registerDate')
    
admin.site.register(ClientContact, HostClientContact)

# department lai register gareko
class HostDepartment(admin.ModelAdmin):
    list_display = ('name', 'email', 'status')
    
admin.site.register(Department, HostDepartment)


# staff lai register gareko
class HostStaff(admin.ModelAdmin):
    list_display = ['firstName', 'middleName', 'lastName', 'deptId', 'email', 'mobile', 'registerDate']
    
admin.site.register(Staff, HostStaff)

# Activities Table lai register gareko
# yo chai mero main ho tyo Activities Table ko aru sabai tyo admin.site.register(Activties, HostActivites haru mailey hataideko) yo matra cha hai
class ActivityInline(admin.StackedInline):
    # fields = ('actId','comment', 'commentBy', 'timeStamp')
    readonly_fields = ('actId','comment', 'commentBy', 'timeStamp')
    model = ActivityTable
    extra = 0

class HostActivities(admin.ModelAdmin):
    list_display = ('title', 'ETA', 'startTime', 'endTime', 'created')
    inlines = [ActivityInline]
    
admin.site.register(Activities, HostActivities)

# POA lai register gareko
class HostPOA(admin.ModelAdmin):
    list_display = ('activityId', 'Engineers','poaDetails', 'poaEntry')
    
    def Engineers(self, obj):
        return ', '.join([x.firstName for x in obj.fieldEngineer.all()])
    
admin.site.register(Poa,HostPOA)

# Email Notification lai regsiter gareko
class HostEmailNotification(admin.ModelAdmin):
    list_display = ['activityId', 'email', 'sendStatus', 'sendTo', 'logTime']
    
admin.site.register(EmailNotification, HostEmailNotification)

# ActivityTable comment wala lai register gareko tara aailey comment gardida huncha kina bhaney activiestable thyakkai activties ko tala dekhaucha
# class HostActivityTable(admin.ModelAdmin):
#     list_display = ['actId','comment', 'commentBy', 'timeStamp']
    
# admin.site.register(ActivityTable, HostActivityTable)