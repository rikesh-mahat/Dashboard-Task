from django.shortcuts import render, redirect
from Models.departments import Departments
# tyo Models ko application_access ko file bata ApplicationAccess bhanney import gareko
from Models.application_access import ApplicationAccess
from django.http import HttpResponse, HttpResponseRedirect
from Models.applications import Applications
from Models.hosts import Hosts
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from Models.staffs import Staffs
from Models.units import Units
from Models.client_services import ClientServices
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from Models.departments import Departments
from Models.serviceTypes import ServiceTypes
from .models import *

from django.db.models import Count
from django.db.models.functions import Trunc

from .emails import send_department_mail
import re

import json
from datetime import datetime, timedelta


from .forms import ActivitiesForm, StaffsForm

from django.db.models import Q



@login_required()
def dashboard(request):
    
    
    host_counts = Hosts.objects.count()
    
    #no. of application counts
    application_counts =  Applications.objects.count()
    department_counts = Departments.objects.count()   
    applications = Applications.objects.all()  
    unit_counts = Units.objects.all()  
    client_services = ClientServices.objects.all()

    

    # Retrieve the start and end dates for the filter from the request
    start_date_filter = request.GET.get('start_date')
    end_date_filter = request.GET.get('end_date')

    
    # Convert the start and end dates to datetime objects
    start_date = datetime.strptime(start_date_filter, '%Y-%m-%d').date() if start_date_filter else None
    
    end_date = datetime.strptime(end_date_filter, '%Y-%m-%d').date() if end_date_filter else None

    current_date = datetime.now().date()
    
    filter_option = request.GET.get('filter_option')
    
    
   
    
    if start_date is None and filter_option != "filter":
        print("this condition is true")
        if filter_option == "today":
            start_date = current_date - timedelta(days=0)
        elif filter_option == "this_week":
            start_date = current_date - timedelta(days=7)
        elif filter_option == "last_week":
            start_date = current_date - timedelta(days=14)
            end_date = current_date - timedelta(days=7)
        else:
            start_date = datetime(datetime.now().year, datetime.now().month, 1).date()
        
    # Calculate the start and end dates for the previous five days
    
    start_date_default = current_date - timedelta(days=9)
    end_date_default = current_date - timedelta(days=0)
    
    
    
    start_date = start_date or start_date_default
    end_date = end_date or end_date_default
    
    # Query the activities for the specified date range and group them by date and status
    activities_count = Activities.objects.filter(created__date__range=[start_date, end_date]) \
        .values('created__date', 'status') \
        .annotate(count=Count('id'))

    # Create a dictionary to store the counts for each day
    activities_counts_dict = {}

    # Iterate over the query results and populate the dictionary
    for activity in activities_count:
        date = activity['created__date']
        status = activity['status']
        count = activity['count']
        
        if date in activities_counts_dict:
            activities_counts_dict[date][status] = count
        else:
            activities_counts_dict[date] = {status: count}

    # Convert the activities counts dictionary to a JSON string
    activities_counts_json = json.dumps({str(date): counts for date, counts in activities_counts_dict.items()})

    
        
    
    client_services = ClientServices.objects.all()
    active_services = client_services.filter(serviceStatus=True).count()
    inactive_services = client_services.filter(serviceStatus=False).count()
    
    client_services_count = client_services.count()
    
    # more_info_dict = {
    #     'Hosts' : host_counts,
    #     'Applications' : application_counts,
    #     'Client Services' : client_services_count
        
    # }
    
    
    print("\tHostName \tApplication Count \tService Count")
    for host in Hosts.objects.all():
        print(f"\t{host.hostname}\t{host.applications_set.count()}\t{host.clientservices_set.count()}")

    context = {
        'active_services': active_services,
        'inactive_services' : inactive_services,
        'hosts' : host_counts,
        'application_counts' : application_counts,
        'Department': department_counts,
        'applications' : applications,
        'unit_counts'  : unit_counts,
        'applications': applications,
        'client_services': client_services,
        'xlabel': json.dumps([str(day) for day in (start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1))]),
        'host_counts': host_counts,
        'activities_counts_json': activities_counts_json,
        'start_date_filter': start_date_filter,
        'end_date_filter': end_date_filter,
        'selected_option' : filter_option,
        'total_host' : Hosts.objects.all()
    }

    return render(request, 'subisu/dashboard.html', context)


@login_required()
def hosts(request):
    
    hosts = Hosts.objects.all()
    context = {
        'hosts' : hosts
    }
    return render(request, 'subisu/host.html', context)



@login_required()
def add_host(request):
    
    if request.method == "POST":
        deviceid = request.POST.get('deviceid')
        hostname = request.POST.get('hostname')
        devicetype = request.POST.get('devicetype')
        popname = request.POST.get('popname')
        pop = request.POST.get('pop')
        pio = request.POST.get('pio')
        model = request.POST.get('model')
        district = request.POST.get('district')
        region = request.POST.get('region')
        province = request.POST.get('province')
        branch = request.POST.get('branch')
        hypervisor = request.POST.get('hypervisor')

        
       
        # create a new Hosts instance
        new_host = Hosts(deviceId=deviceid, hostname=hostname, deviceType=devicetype, popName=popname,
                          popLatitude=pop, pioLatitude=pio, modelName=model, districtname=district,
                          regionName=region, provinceName=province, branchName=branch, hyperVisor=hypervisor)
        
        # save the new instance to the database
        new_host.save()
        
        # redirect to the hosts list page
        return redirect('hosts')

    return render(request, 'subisu/addhost.html')

def delete_host(request, id):
    host = Hosts.objects.get(id = id)
    host.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = User.objects.filter(username = email)
        if not user.exists():
            messages.error(request,"User Doesn't exist")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
          
        
        
        user = authenticate(username = email, password = password)
        
        
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.warning(request, "Sorry the Credentials do not match")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
    return render(request, 'subisu/login.html')



def logout_user(request):
    messages.info(request, "Thank you for using CMS. Sign in again")
    logout(request)
    return redirect('login')
    


def register_user(request):
    
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        email =  request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        
        user = User.objects.filter(username = username) 
        if user.exists():
            messages.error(request, "Sorry the username is already taken")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        user = User.objects.filter(email = email)
        if user.exists():
            messages.error(request, "Sorry the email is already in use")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if len(pass1) < 8:
            messages.warning(request, "Password should be minimum 8 Characters long")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if pass1 != pass2:
            messages.warning(request, "Password do not match")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        user = User.objects.create(first_name = fname, last_name = lname, username = username, email = email, is_superuser = True, is_staff=True)
        user.set_password(pass2)
        user.save()
        
        return redirect('admins')

    return render(request, 'subisu/signup.html')


def display_admin(request):
    keyword = request.GET.get('keyword')
    admins = User.objects.filter(is_superuser=True)

    if keyword:
        admins = admins.filter(
            Q(first_name__icontains=keyword) |
            Q(last_name__icontains=keyword) |
            Q(username__icontains=keyword) |
            Q(email__icontains=keyword)
        )

    context = {
        'admins': admins
    }
    
    return render(request, 'subisu/admin.html', context)

def edit_admin(request, id):
    user = User.objects.get(id = id)
    return render(request, 'subisu/editadmin.html', {'user' : user})



def activities(request):
    activities = Activities.objects.all().order_by('-created')
    context = {
        'activities' : activities
    }
    return render(request, 'subisu/activities.html', context)

def process_emails(primary_email, other_emails):
    # split string by comma or space
    emails = re.split(r',|\s', other_emails)
    
    # filter out any empty strings
    emails = filter(lambda x: x != '', emails)
    
    # validate each email using regex
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    valid_emails = filter(lambda x: re.match(email_regex, x), emails)
    
    # convert valid emails to a list
    email_list = list(valid_emails)
    email_list.append(primary_email)
    
    return email_list

def create_acitivities(request):
    if request.method == "POST":
        form  = ActivitiesForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.save()
            if form.cleaned_data['sendEmail']:
                title = form.cleaned_data['title']
                location = form.cleaned_data['location']
                reason = form.cleaned_data['reason']
                benefits = form.cleaned_data['benefits']
                impact = form.cleaned_data['impact']
                primary_email = form.cleaned_data['contact']
                # retrieve otherEmails value from cleaned_data
                other_emails = form.cleaned_data['otherEmails']
                
                email_list = process_emails(primary_email, other_emails)
                EmailNotification.objects.create(activityId = activity, emailBody = " \n".join([title, location, benefits, reason, impact]))
                
                msg = send_department_mail(title,"time",location, reason, benefits, impact, email_list)
                if msg:
                    messages.info(request, "Mail sent successfully")
                else:
                    messages.warning(request, "Sorry, Mail not sent due to error")
            form.save()
            return redirect('activities')
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field_name}: {error}")
    else:
        form = ActivitiesForm()
    context  = {
        'form' : form
    }
    
    return render(request, 'subisu/addactivities.html', context)


def edit_activities(request, id):
    activity = Activities.objects.get(id = id)
    if request.method == "POST":
        form = ActivitiesForm(request.POST, instance=activity)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.save()
            if form.cleaned_data['sendEmail']:
                title = form.cleaned_data['title']
                location = form.cleaned_data['location']
                reason = form.cleaned_data['reason']
                benefits = form.cleaned_data['benefits']
                impact = form.cleaned_data['impact']
                primary_email = form.cleaned_data['contact']
                # retrieve otherEmails value from cleaned_data
                other_emails = form.cleaned_data['otherEmails']
                
                email_list = process_emails(primary_email, other_emails)
                EmailNotification.objects.create(activityId = activity, emailBody = " \n".join([title, location, benefits, reason, impact]))
                msg = send_department_mail(title,"time",location, reason, benefits, impact, email_list)
                if msg:
                    messages.info(request, "Mail sent successfully")
                else:
                    messages.warning(request, "Sorry, Mail not sent due to error")
            form.save()
            return redirect('activities')
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field_name}: {error}")
    else:
        form = ActivitiesForm(instance=activity)
    context = {
        'form': form,
        'activity_id': id
    }
    return render(request, 'subisu/addactivities.html', context)


def send_activities_mail(request, id):
    
    actvitiy = Activities.objects.get(id = id)
 
    title = actvitiy.title
    location = actvitiy.location
    benefits = actvitiy.benefits
    reason = actvitiy.reason
    impact = actvitiy.impact
    contact = actvitiy.contact
    other_emails = actvitiy.otherEmails
    
    email_list = process_emails(contact, other_emails)            
    msg = send_department_mail(title,"time",location, reason, benefits, impact, email_list)
    
    
    EmailNotification.objects.create(activityId = actvitiy, emailBody = " \n".join([title, location, benefits, reason, impact]))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def delete_activity(request, id):
    
    activity = Activities.objects.get(id=id)
    activity.delete()
    messages.info(request, "Deleted the activity successfully")
    return redirect('activities')



def display_staffs(request):
    staffs = Staffs.objects.all()
    context = {
        'staffs' : staffs
    }
    return render(request, 'subisu/staffs.html', context)


def delete_staff(request, id):
    staff = Staffs.objects.get(id = id)
    staff.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def create_staff(request):
    if request.method == 'POST':
        print("form is working")
        form = StaffsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staffs')  
    else:
        form = StaffsForm()
    
    context = {
        'form': form
        }
    

    return render(request, 'subisu/addstaff.html', context)




def view_emails(request):
    emails = EmailNotification.objects.all()
    context = {
        'emails' : emails
    }
    return render(request, 'subisu/emails.html', context)


def user_profile(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        
        user = User.objects.get(username = username)
        user.first_name = fname
        user.last_name = lname
        user.username = username
        user.email = email
        user.save()
        
        return redirect('dashboard')
        
        
    return render(request, 'subisu/profile.html')




def applications(request):
    applications = Applications.objects.all()
    context = {
        'applications' : applications
    }

    return render(request, 'subisu/applications.html', context)