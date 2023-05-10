from django import forms
from Models.departments import Departments
from .models import *
from Models.staffs import Staffs
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
        model = Activities
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'benefits': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'impact': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contact': forms.Select(attrs={'class': 'form-control'}),
            'startTime': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'data-target' : '#datetimepicker1'}),
            'endTime': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'data-target' : '#datetimepicker2'}),
            'activities': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'otherEmails': forms.TextInput(attrs={'class': 'form-control'}),
            'Comment': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            
        }

        
        
class StaffsForm(forms.ModelForm):
    
    class Meta:
        model = Staffs
        fields = '__all__'
        
        widgets = {
            'firstName': forms.TextInput(attrs={'class': 'form-control'}),
            'middleName': forms.TextInput(attrs={'class': 'form-control'}),
            'lastName': forms.TextInput(attrs={'class': 'form-control'}),
            'empId': forms.TextInput(attrs={'class': 'form-control'}),
            'unitId': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),   
        }   
        