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


admin.site.register([Priviliges])

@admin.register(Units)
class AdminUnit(admin.ModelAdmin):
    list_display = ['name', 'departmentId', 'unitHead', 'email']

    
@admin.register(ApplicationAccess)
class ApplicationAccessAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'applicationId', 'applicationAccountStatus']
    
    def get_full_name(self, obj):
        return f"{obj.userId.firstName} {obj.userId.middleName} {obj.userId.lastName}" if obj.userId.middleName else obj.userId.firstName + " " + obj.userId.lastName
    get_full_name.short_description = 'User'
    
    search_fields = ['userId__firstName', 'userId__middleName', 'userId__lastName']
    


@admin.register(Applications)
class AdminApplication(admin.ModelAdmin):
    list_display = ['name', 'url', 'language', 'serverAccess', 'serverControl', 'hostId']

    def language(self, obj):
        return obj.devLanguage
    language.short_description = "Development Language"



@admin.register(Hosts)
class AdminHosts(admin.ModelAdmin):

    
    list_display= ['hostname', 'deviceType', 'popName', 'popLatitude', 'longitude', 'modelName', 'districtname', 'regionName', 'provinceName', 'branchName', 'hyperVisor']
    
    def longitude(self, obj):
        return obj.pioLatitude
    longitude.short_description = "popLongitude"
    
    
@admin.register(ServiceTypes)
class AdminServiceTypes(admin.ModelAdmin):
    list_display = ['srv', 'description']
    
    def srv(self, obj):
        return obj.srvType
    srv.short_description = "Service Type"
    
    
@admin.register(Staffs)
class AdminStaff(admin.ModelAdmin):

    list_display = ['user', 'firstName', 'middleName', 'lastName', 'Id', 'unitId', 'email', 'status']
    
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
    # domainName = models.CharField(max_length=250)
    # srvType = models.ForeignKey(ServiceTypes, on_delete=models.PROTECT)
    # hostId = models.ForeignKey(Hosts, on_delete=models.PROTECT)
    # # email = models.EmailField()
    # primaryContactName = models.CharField(max_length=250)
    # primaryContactNumber = models.BigIntegerField(validators=[mobile_number_validation])
    # primaryContactEmail = models.EmailField()
    # secondaryContactName =models.CharField(max_length=250)
    # secondaryContactNumber = models.BigIntegerField(validators=[mobile_number_validation])
    # secondaryContactEmail = models.EmailField()
    # serviceStatus = models.BooleanField(default = True)
    # serviceCreatedDate = models.DateTimeField()
    list_display = ['domainName', 'srv', 'hostId', 'primaryContactName', 'primaryContactNumber', 'primaryContactEmail', 'secondaryContactName', 'secondaryContactNumber', 'secondaryContactEmail',
                    'serviceStatus', 'serviceCreatedDate']
    def srv(self, obj):
        return obj.srvType
    srv.short_description = "Service"