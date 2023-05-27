from Models.units import Units
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from Models.application_access import ApplicationAccess

@admin.register(Units)
class AdminUnit(ImportExportModelAdmin):
    list_display = ['name', 'departmentId', 'unitHead', 'email']
    
@admin.register(ApplicationAccess)
class ApplicationAccessAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'applicationId', 'applicationAccountStatus']
    
    def get_full_name(self, obj):
        return f"{obj.userId.firstName} {obj.userId.middleName} {obj.userId.lastName}" if obj.userId.middleName else obj.userId.firstName + " " + obj.userId.lastName
    get_full_name.short_description = 'User'
    
    search_fields = ['userId__firstName', 'userId__middleName', 'userId__lastName']