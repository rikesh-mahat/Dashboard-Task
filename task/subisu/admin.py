from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register([ServiceType])


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


class HostDataCenter(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact')
    
    
admin.site.register(Datacenter, HostDataCenter)


class HostClientContact(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'email', 'status', 'registerDate')
    
admin.site.register(ClientContact, HostClientContact)


class HostDepartment(admin.ModelAdmin):
    list_display = ('name', 'email', 'status')
    
admin.site.register(Department, HostDepartment)


class HostStaff(admin.ModelAdmin):
    list_display = ['firstName', 'middleName', 'lastName', 'deptId', 'email', 'mobile', 'registerDate']
    
admin.site.register(Staff, HostStaff)

class HostActivities(admin.ModelAdmin):
    list_display =  ('title', 'startTime', 'endTime', 'created')

admin.site.register(Activities,HostActivities)


class HostPOA(admin.ModelAdmin):
    list_display = ('activityId', 'Engineers','poaDetails', 'poaEntry')
    
    def Engineers(self, obj):
        return ', '.join([x.firstName for x in obj.fieldEngineer.all()])
    
admin.site.register(Poa,HostPOA)


class HostEmailNotification(admin.ModelAdmin):
    list_display = ['activityId', 'email', 'sendStatus', 'logTime']
    
admin.site.register(EmailNotification, HostEmailNotification)