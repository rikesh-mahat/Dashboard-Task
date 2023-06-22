# from Models.units import Units

# from django.contrib import admin
# from Models.application_access import ApplicationAccess
# from Models.previliges import Priviliges
# from Models.applications import Applications
# from Models.hosts import Hosts
# from Models.client_services import ClientServices
# from Models.departments import Departments
# from Models.staffs import Staffs
# from Models.serviceTypes import ServiceTypes


# admin.site.register([Priviliges])

# @admin.register(Units)
# class AdminUnit(admin.ModelAdmin):
#     list_display = ['name', 'departmentId', 'unitHead', 'email']

    
# @admin.register(ApplicationAccess)
# class ApplicationAccessAdmin(admin.ModelAdmin):
#     list_display = ['get_full_name', 'applicationId', 'applicationAccountStatus']
    
#     def get_full_name(self, obj):
#         return f"{obj.userId.firstName} {obj.userId.middleName} {obj.userId.lastName}" if obj.userId.middleName else obj.userId.firstName + " " + obj.userId.lastName
#     get_full_name.short_description = 'User'
    
#     search_fields = ['userId__firstName', 'userId__middleName', 'userId__lastName']
    


# @admin.register(Applications)
# class AdminApplication(admin.ModelAdmin):
#     list_display = ['name', 'url', 'language', 'serverAccess', 'serverControl', 'hostId']

#     def language(self, obj):
#         return obj.devLanguage
#     language.short_description = "Development Language"



# @admin.register(Hosts)
# class AdminHosts(admin.ModelAdmin):

    
#     list_display= ['hostname', 'deviceType', 'popName', 'popLatitude', 'longitude', 'modelName', 'districtname', 'regionName', 'provinceName', 'branchName', 'hyperVisor']
    
#     def longitude(self, obj):
#         return obj.pioLatitude
#     longitude.short_description = "popLongitude"
    
    
# @admin.register(ServiceTypes)
# class AdminServiceTypes(admin.ModelAdmin):
#     list_display = ['srv', 'description']
    
#     def srv(self, obj):
#         return obj.srvType
#     srv.short_description = "Service Type"
    
    
# @admin.register(Staffs)
# class AdminStaff(admin.ModelAdmin):

#     list_display = ['user', 'firstName', 'middleName', 'lastName', 'Id', 'unitId', 'email', 'status']
    
#     def Id(self, obj):
#         return obj.empId
#     Id.short_description = "Employee Id"
    


# @admin.register(Departments)
# class AdminDepartments(admin.ModelAdmin):

    
#     list_display = ['name', 'Email', 'status', 'vp']
    
#     def vp(self, obj):
#         return obj.vpName
#     vp.short_description = "Vice President"
    
    
# @admin.register(ClientServices)
# class AdminClientServices(admin.ModelAdmin):
#     list_display = ['domainName', 'srv', 'hostId', 'primaryContactName', 'primaryContactNumber', 'primaryContactEmail', 'secondaryContactName', 'secondaryContactNumber', 'secondaryContactEmail',
#                     'serviceStatus', 'serviceCreatedDate']
#     def srv(self, obj):
#         return obj.srvType
#     srv.short_description = "Service"


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
from import_export.admin import ImportExportModelAdmin




class PriviligesAdmin(ImportExportModelAdmin):
    list_display = ('preLevel', 'description')
    search_fields = ('preLevel', 'description')

admin.site.register(Priviliges, PriviligesAdmin)


class UnitsAdmin(admin.ModelAdmin):
    list_display = ('name', 'departmentId', 'unitHead', 'email', 'status')
    list_filter = ('departmentId', 'status')
    search_fields = ('name', 'unitHead', 'email')
    readonly_fields = ('departmentId',)  # Assuming you want the departmentId field to be read-only
    fieldsets = (
        ('Unit Information', {
            'fields': ('name', 'departmentId', 'unitHead')
        }),
        ('Contact Information', {
            'fields': ('email',)
        }),
        ('Status', {
            'fields': ('status',)
        })
    )

admin.site.register(Units, UnitsAdmin)


    
@admin.register(ApplicationAccess)
class ApplicationAccessAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'applicationId', 'applicationAccountStatus']
    search_fields = ['userId_firstName', 'userIdmiddleName', 'userId_lastName']
    
    
    def get_full_name(self, obj):
        return f"{obj.userId.firstName} {obj.userId.middleName} {obj.userId.lastName}" if obj.userId.middleName else obj.userId.firstName + " " + obj.userId.lastName
    get_full_name.short_description = 'User'
    


@admin.register(Applications)
class AdminApplication(ImportExportModelAdmin):
    list_display = ['name', 'url', 'language', 'serverAccess', 'serverControl', 'hostId']
    search_fields = ['name', 'hostId'] 

    def language(self, obj):
        return obj.devLanguage
    language.short_description = "Development Language"



@admin.register(Hosts)
class AdminHosts(ImportExportModelAdmin):

    
    list_display= ['hostname', 'deviceType', 'popName', 'popLatitude', 'longitude', 'modelName', 'districtname', 'regionName', 'provinceName', 'branchName', 'hyperVisor']
    search_fields = ['hostname', 'modelName']
    
    def longitude(self, obj):
        return obj.pioLatitude
    longitude.short_description = "popLongitude"
    
    
@admin.register(ServiceTypes)
class AdminServiceTypes(ImportExportModelAdmin):
    list_display = ['srv', 'description']
    
    def srv(self, obj):
        return obj.srvType
    srv.short_description = "Service Type"
    
    
@admin.register(Staffs)
class AdminStaff(ImportExportModelAdmin):

    list_display = ['user', 'firstName', 'middleName', 'lastName', 'Id', 'unitId', 'email', 'status']
    list_filter = ('unitId', 'status')
    search_fields = ('firstName', 'lastName', 'empId', 'email')
    readonly_fields = ('user',)  

    
    def Id(self, obj):
        return obj.empId
    Id.short_description = "Employee Id"
    


@admin.register(Departments)
class AdminDepartments(admin.ModelAdmin):

    
    list_display = ['name', 'Email', 'status', 'vp']
    
    def vp(self, obj):
        return obj.vpName
    vp.short_description = "Vice President"
    
    
@admin.register(ClientServices)
class AdminClientServices(admin.ModelAdmin):

    list_display = ['domainName', 'srv', 'hostId', 'primaryContactName', 'primaryContactNumber', 'primaryContactEmail', 'secondaryContactName', 'secondaryContactNumber', 'secondaryContactEmail',
                    'serviceStatus', 'serviceCreatedDate']
    def srv(self, obj):
        return obj.srvType
    srv.short_description = "Service"