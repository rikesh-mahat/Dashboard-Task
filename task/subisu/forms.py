from django import forms
from Models.departments import Departments
from .models import *
class DepartmentsForm(forms.ModelForm):
    class Meta:
        model = Departments
        fields = ('name', 'Email', 'status', 'vpName')
        labels = {
            'name': 'Name',
            'Email': 'Email',
            'status': 'Status',
            'vpName': 'Vice-president Name'
        }
        
        
class ActivitiesForm(forms.ModelForm):
    class Meta:
        model  = Activities
        fields = '__all__'
        