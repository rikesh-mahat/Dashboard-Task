from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib import admin
from Models.application_access import ApplicationAccess
from Models.previliges import Priviliges
from Models.applications import Applications
from Models.hosts import Hosts
from Models.client_services import ClientServices
from Models.departments import Departments
from Models.staffs import Staffs
from Models.serviceTypes import ServiceTypes
from Models.units import Units

admin.site.register([ApplicationAccess, Priviliges, Applications, Hosts, ClientServices, Departments, Staffs, ServiceTypes, Units])

# services ra host lai register gareko
class ServiceInline(admin.StackedInline):
    model = Service
    extra = 0


# datacenter table lai register gareko
class HostDataCenter(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact')
    
    
admin.site.register(Datacenter, HostDataCenter)

# client table lai register gareko
class HostClientContact(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'email', 'status', 'registerDate')
    
admin.site.register(ClientContact, HostClientContact)

class ActivityInline(admin.StackedInline):
    readonly_fields = ('actId','comment', 'commentBy', 'timeStamp')
    model = ActivityTable
    extra = 0

class HostActivities(admin.ModelAdmin):
    list_display = ('id', 'title','startTime', 'endTime', 'created')
    inlines = [ActivityInline]
    
admin.site.register(Activities, HostActivities)


class HostPOA(admin.ModelAdmin):
    list_display = ('id', 'activityId', 'Engineers','poaDetails', 'poaEntry')
    
    def Engineers(self, obj):
        return ', '.join([x.firstName for x in obj.fieldEngineer.all()])
    
admin.site.register(Poa,HostPOA)


class HostEmailNotification(admin.ModelAdmin):
    list_display = ['activityId', 'emailBody', 'logTime']
    
admin.site.register(EmailNotification, HostEmailNotification)


