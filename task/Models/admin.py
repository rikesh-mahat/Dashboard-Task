from Models.units import Units

from django.contrib import admin
from Models.application_access import ApplicationAccess
from Models.previliges import Priviliges
from Models.applications import Applications
from Models.hosts import Hosts
from Models.client_services import ClientServices
from Models.departments import Departments
from Models.staffs import Staffs
from Models.serviceTypes import ServiceTypes
from Models.branch import Branch

@admin.register(Units)
class AdminUnit(admin.ModelAdmin):
    list_display = ['name', 'departmentId', 'unitHead', 'email']
    list_filter = ('name', 'departmentId')
    search_fields = ('name', 'unitHead')

    
@admin.register(ApplicationAccess)
class ApplicationAccessAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'applicationId', 'applicationAccountStatus']
    
    def get_full_name(self, obj):
        return f"{obj.userId.firstName} {obj.userId.middleName} {obj.userId.lastName}" if obj.userId.middleName else obj.userId.firstName + " " + obj.userId.lastName
    get_full_name.short_description = 'User'
    
    search_fields = ['userId__firstName', 'userId__middleName', 'userId__lastName']

class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'branch_type', 'address', 'contact', 'longitude', 'latitude', 'ip_address', 'remarks')
    list_filter = ('branch_type', 'contact')
    search_fields = ('branch_type', 'address')

admin.site.register(Branch, BranchAdmin)


class PriviligesAdmin(admin.ModelAdmin):
    list_display = ('id', 'preLevel', 'description')
    search_fields = ('preLevel', 'id')

admin.site.register(Priviliges, PriviligesAdmin)


class ApplicationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'devLanguage', 'sourceCode', 'serverAccess', 'serverControl', 'hostId')
    list_filter = ('devLanguage', 'serverControl')
    search_fields = ('name', 'url')

admin.site.register(Applications, ApplicationsAdmin)


class HostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'hostname', 'deviceType', 'popName', 'modelName', 'branchName')
    search_fields = ('hostname', 'deviceType', 'popName', 'modelName', 'branchName')
    list_filter = ('deviceType', 'popName', 'modelName', 'branchName')

admin.site.register(Hosts, HostsAdmin)



class ClientServicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'domainName', 'srvType', 'hostId', 'primaryContactName', 'primaryContactNumber', 'primaryContactEmail', 'secondaryContactName', 'secondaryContactNumber', 'secondaryContactEmail', 'serviceStatus', 'serviceCreatedDate')
    search_fields = ('domainName', 'primaryContactName', 'primaryContactEmail', 'secondaryContactName', 'secondaryContactEmail')
    list_filter = ('srvType', 'hostId', 'serviceStatus')
    readonly_fields = ('serviceCreatedDate',)

admin.site.register(ClientServices, ClientServicesAdmin)


class DepartmentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'Email', 'status', 'vpName')
    search_fields = ('name', 'Email', 'vpName')
    list_filter = ('status',)
    readonly_fields = ('name',)

admin.site.register(Departments, DepartmentsAdmin)


class StaffsAdmin(admin.ModelAdmin):
    list_display = ('firstName', 'middleName', 'lastName', 'empId', 'unitId', 'email', 'status')
    search_fields = ('firstName', 'middleName', 'lastName', 'empId', 'email')
    list_filter = ('status',)
    # autocomplete_fields = ('unitId',)

admin.site.register(Staffs, StaffsAdmin)



class ServiceTypesAdmin(admin.ModelAdmin):
    list_display = ('srvType', 'description')

admin.site.register(ServiceTypes, ServiceTypesAdmin)






    