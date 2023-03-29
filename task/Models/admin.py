from Models.units import Units
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

@admin.register(Units)
class AdminUnit(ImportExportModelAdmin):
    list_display = ['name', 'departmentId', 'unitHead', 'email']
    
    
    