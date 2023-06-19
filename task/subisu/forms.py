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
        exclude = ['contact']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
            'location': forms.TextInput(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
            'reason': forms.Textarea(attrs={'class': 'input-group input-group-outline my-3 border rounded', 'rows': 3}),
            'impact': forms.Textarea(attrs={'class': 'input-group input-group-outline my-3 border rounded', 'rows': 3}),
            'contact': forms.Select(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
            'startTime': DateTimePickerInput(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
            'endTime': DateTimePickerInput(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
            'activities': forms.Textarea(attrs={'class': 'input-group input-group-outline my-3 border rounded', 'rows': 5}),
            'otherEmails': forms.TextInput(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
            'Comment': forms.TextInput(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
            'status': forms.Select(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
        }


        
        
class StaffsForm(forms.ModelForm):
    
    class Meta:
        model = Staffs
        exclude = ['user']
        
        widgets = {
            'user' : forms.Select(attrs={'class' : 'input-group input-group-outline my-3 border rounded'}),
            'firstName': forms.TextInput(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
            'middleName': forms.TextInput(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
            'lastName': forms.TextInput(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
            'empId': forms.TextInput(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
            'unitId': forms.Select(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
            'email': forms.TextInput(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),   
        }   
        


class PoaForm(forms.ModelForm):
    class Meta:
        model = Poa
        fields = '__all__'
        widgets = {
            'activityId': forms.Select(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
            'fieldEngineer': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'poaDetails': forms.Textarea(attrs={'class': 'input-group input-group-outline my-3 border rounded', 'rows': 3}),
            'units': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'sendEmail': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        




class DepartmentsForm(forms.ModelForm):
    class Meta:
        model = Departments
        fields = ['name', 'Email', 'status', 'vpName']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
            'Email': forms.EmailInput(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
            'status': forms.CheckboxInput(attrs={'class': 'custom-checkbox'}),
            'vpName': forms.TextInput(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
        }


from Models.applications import Applications

class ApplicationsForm(forms.ModelForm):
    class Meta:
        model = Applications
        fields = ['name', 'url', 'devLanguage', 'sourceCode', 'serverAccess', 'serverControl', 'hostId']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
            'url': forms.URLInput(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
            'devLanguage': forms.TextInput(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
            'sourceCode': forms.Select(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
            'serverAccess': forms.TextInput(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
            'serverControl': forms.Select(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
            'hostId': forms.Select(attrs={'class': 'input-group input-group-outline my-3 border rounded'}),
        }
