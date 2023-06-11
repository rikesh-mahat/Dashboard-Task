from django import forms
from Models.departments import Departments
from .models import *
from Models.staffs import Staffs
from django_flatpickr.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput

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
            'startTime': DateTimePickerInput(attrs={'class': 'form-control'}),
            'endTime': DateTimePickerInput(attrs={'class': 'form-control'}),
            'activities': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'otherEmails': forms.TextInput(attrs={'class': 'form-control'}),
            'Comment': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


        
        
class StaffsForm(forms.ModelForm):
    
    class Meta:
        model = Staffs
        exclude = ['user']
        
        widgets = {
            'user' : forms.Select(attrs={'class' : 'form-control'}),
            'firstName': forms.TextInput(attrs={'class': 'form-control'}),
            'middleName': forms.TextInput(attrs={'class': 'form-control'}),
            'lastName': forms.TextInput(attrs={'class': 'form-control'}),
            'empId': forms.TextInput(attrs={'class': 'form-control'}),
            'unitId': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),   
        }   
        


class PoaForm(forms.ModelForm):
    class Meta:
        model = Poa
        fields = '__all__'
        widgets = {
            'activityId': forms.Select(attrs={'class': 'form-control'}),
            'fieldEngineer': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'poaDetails': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'units': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'sendEmail': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        




class DepartmentsForm(forms.ModelForm):
    class Meta:
        model = Departments
        fields = ['name', 'Email', 'status', 'vpName']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'Email': forms.EmailInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'custom-checkbox'}),
            'vpName': forms.TextInput(attrs={'class': 'form-control'}),
        }


from Models.applications import Applications

class ApplicationsForm(forms.ModelForm):
    class Meta:
        model = Applications
        fields = ['name', 'url', 'devLanguage', 'sourceCode', 'serverAccess', 'serverControl', 'hostId']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'devLanguage': forms.TextInput(attrs={'class': 'form-control'}),
            'sourceCode': forms.Select(attrs={'class': 'form-control'}),
            'serverAccess': forms.TextInput(attrs={'class': 'form-control'}),
            'serverControl': forms.Select(attrs={'class': 'form-control'}),
            'hostId': forms.Select(attrs={'class': 'form-control'}),
        }
