# from django.contrib import admin
# from .models import *
# # Register your models here.
# from django.contrib import admin


# # from import_export.admin import ImportExportModelAdmin



# # services ra host lai register gareko
# class ServiceInline(admin.StackedInline):
#     model = Service
#     extra = 0


# # datacenter table lai register gareko
# class HostDataCenter(admin.ModelAdmin):
#     list_display = ('name', 'address', 'contact')
    
    
# admin.site.register(Datacenter, HostDataCenter)

# # client table lai register gareko
# class HostClientContact(admin.ModelAdmin):
#     list_display = ('name', 'mobile', 'email', 'status', 'registerDate')
    
# admin.site.register(ClientContact, HostClientContact)

# class ActivityInline(admin.StackedInline):
    
#     model = ActivityTable
#     extra = 0


# class POAInline(admin.StackedInline):
#     model = Poa
#     extra = 0
    
# class HostActivities(admin.ModelAdmin):
#     list_display = ('id', 'title', 'ETA','startTime', 'endTime', 'created')
#     inlines = [ActivityInline, POAInline]
    
# admin.site.register(Activities, HostActivities)


# # class HostPOA(admin.ModelAdmin):
# #     list_display = ('id', 'activityId', 'Engineers','poaDetails', 'poaEntry')
    
# #     def Engineers(self, obj):
# #         return ', '.join([x.firstName for x in obj.fieldEngineer.all()])
    
# # admin.site.register(Poa,HostPOA)


# class HostEmailNotification(admin.ModelAdmin):
#     list_display = ['activityId', 'emailBody', 'logTime']
    
# admin.site.register(EmailNotification, HostEmailNotification)


from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin


# from import_export.admin import ImportExportModelAdmin



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
    
    model = ActivityTable
    extra = 0


class POAInline(admin.StackedInline):
    model = Poa
    extra = 0
    


class ActivitiesAdmin(ImportExportModelAdmin):
    list_display = ('title', 'empId', 'location', 'status', 'created')
    list_filter = ('status', 'created')
    search_fields = ('title', 'location')
    date_hierarchy = 'created'
    readonly_fields = ('created',)
    fieldsets = (
        ('Activity Information', {
            'fields': ('title', 'empId', 'location', 'reason', 'impact')
        }),
        ('Time Information', {
            'fields': ('startTime', 'endTime')
        }),
        ('Contact Information', {
            'fields': ('contact', 'otherEmails', 'sendEmail')
        }),
        ('Additional Information', {
            'fields': ('Comment', 'status', 'ETA')
        })
    )

admin.site.register(Activities, ActivitiesAdmin)


# class HostPOA(admin.ModelAdmin):
#     list_display = ('id', 'activityId', 'Engineers','poaDetails', 'poaEntry')
    
#     def Engineers(self, obj):
#         return ', '.join([x.firstName for x in obj.fieldEngineer.all()])
    
# admin.site.register(Poa,HostPOA)


class HostEmailNotification(admin.ModelAdmin):
    list_display = ['activityId', 'emailBody', 'logTime']
    
admin.site.register(EmailNotification, HostEmailNotification)