from django.shortcuts import render, redirect
from Models.departments import Departments
# tyo Models ko application_access ko file bata ApplicationAccess bhanney import gareko
from Models.application_access import ApplicationAccess
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
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


from .forms import *

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
    
    
  
    context = {
        'active_services': active_services,
        'inactive_services' : inactive_services,
        'hosts' : host_counts,
        'services' : client_services_count,
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

@login_required()
def delete_host(request, id):
    host = Hosts.objects.get(id = id)
    host.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



from django.contrib.auth.models import User

from django.contrib.auth.models import User

def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        session_username = request.session.get('email', None)
        user = User.objects.filter(username=email).first()  # Retrieve the user
        if not user:
            messages.error(request, "User doesn't exist")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if not user.is_staff:
            messages.warning(request, "Sorry, your account has been deactivated")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if session_username is not None and session_username == email:
            attempts = request.session.get('attempts', 0)
            if attempts >= 4:
                user.is_staff = False
                user.save()
                messages.error(request, "Sorry, your account has been disabled for incorrect attempts")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            attempts += 1
            request.session['attempts'] = attempts
        else:
            request.session['attempts'] = 1  # Reset the attempts if a different user is logging in
            request.session['email'] = email

        user = authenticate(username=email, password=password)

        if user:
            login(request, user)
            request.session['attempts'] = 0  # Reset the attempts on successful login
            return redirect('dashboard')
        else:
            messages.warning(request, "Sorry, the credentials do not match")
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

@login_required()
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
@login_required()
def edit_admin(request, id):
    user = User.objects.get(id = id)
    return render(request, 'subisu/editadmin.html', {'user' : user})


@login_required()
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

@login_required()
def create_acitivities(request):
    if request.method == "POST":
        context = {}
        form = ActivitiesForm(request.POST)
        
        if form.is_valid():
            activity = form.save(commit=False)
            start_time = form.cleaned_data['startTime']
            end_time = form.cleaned_data['endTime']

            if start_time is None or end_time is None:
                messages.info(request,"Please choose a start time and end time")
                context['form'] = form
                return render(request, 'subisu/addactivities.html', context)
            

            
            if end_time < start_time:
                messages.warning(request, "End time cannot be earlier than start time")
                context['form'] = form
                return render(request, 'subisu/addactivities.html', context)
            
            activity.save()
            
            comment = form.cleaned_data['Comment']

            staff_name = request.user.username  # Default to username if staff attribute is not available

            if request.user.is_authenticated and hasattr(request.user, 'staff'):
                staff = request.user.staff
                staff_name = staff.firstName + " " + staff.middleName + " " +  staff.lastName if staff.middleName else  staff.firstName + " " +  staff.lastName
            staff_name = request.user.username
            ActivityTable.objects.create(actId=activity, comment=comment, commentBy=staff_name)
            
            
            if 'send_email' in form.cleaned_data and form.cleaned_data['send_email']:
                title = form.cleaned_data['title']
                location = form.cleaned_data['location']
                reason = form.cleaned_data['reason']
                benefits = form.cleaned_data['benefits']
                impact = form.cleaned_data['impact']
                primary_email = form.cleaned_data['contact']
                other_emails = form.cleaned_data['otherEmails']
                email_list = process_emails(primary_email, other_emails)
                EmailNotification.objects.create(activityId=activity, emailBody="\n".join([title, location, benefits, reason, impact]))
                msg = send_department_mail(title, "time", location, reason, benefits, impact, email_list)
                if msg:
                    messages.info(request, "Mail sent successfully")
                else:
                    messages.warning(request, "Sorry, Mail not sent due to an error")
            return redirect('create_poa')
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field_name}: {error}")
    else:
        form = ActivitiesForm()

    activities = Activities.objects.filter(Q(status=ACTIVITY_STATUS[0][0]) | Q(status=ACTIVITY_STATUS[1][0]))
    field_engineers = Staffs.objects.filter(status=True)
    units = Units.objects.filter(status=True)

    context = {
        'form': form,
        'activities': activities,
        'field_engineers': field_engineers,
        'units': units
    }

    return render(request, 'subisu/addactivities.html', context)

@login_required()
def edit_activities(request, id):
    activity = Activities.objects.get(id = id)
    comments = ActivityTable.objects.filter(actId = activity)
    
    
    start_time = activity.startTime
    end_time = activity.endTime
    
    
    if request.method == "POST":
        form = ActivitiesForm(request.POST, instance=activity)
        
        if form.is_valid():
            activity = form.save(commit=False)
            activity.startTime = start_time
            activity.endTime = end_time
            new_start_time  = form.cleaned_data['startTime']
            new_end_time = form.cleaned_data['endTime']
            
            if start_time != new_start_time and new_start_time is not None:
                activity.startTime = new_start_time
            
            if end_time != new_end_time and new_end_time is not None:
                activity.endTime = new_end_time
            
            activity.save()
            

            
            
            
            

            comment = activity.Comment.strip()
            last_comment_instance = ActivityTable.objects.filter(actId=activity).last()
            previous_comment = last_comment_instance.comment.strip()
            pattern = re.escape(previous_comment)

          
            if comment is not None and  not re.search(pattern, comment):
                print("it is working lol")
                try:
                    staff = request.user.staff
                    staff_name = staff.firstName + " " + staff.middleName + " " + staff.lastName if staff.middleName else staff.firstName + " " + staff.lastName
                except AttributeError:
                    staff_name = request.user.username

                ActivityTable.objects.create(actId=activity, comment=comment, commentBy=staff_name)
            
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
        'activity_id': id,
        'comments' : comments
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


@login_required()
def delete_activity(request, id):
    
    activity = Activities.objects.get(id=id)
    activity.delete()
    messages.info(request, "Deleted the activity successfully")
    return redirect('activities')


@login_required()
def display_staffs(request):
    staffs = Staffs.objects.all()
    context = {
        'staffs' : staffs
    }
    return render(request, 'subisu/staffs.html', context)

@login_required()
def delete_staff(request, id):
    staff = Staffs.objects.get(id = id)
    staff.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

from django.contrib.auth.decorators import login_required

@login_required
def create_staff(request):
    if request.method == 'POST':
        form = StaffsForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            users = User.objects.filter(Q(email=username) | Q(username=username))
            if users.exists():
                messages.warning(request, "Sorry, the email is already in use")
                return redirect('add_staff') 
            new_staff_user = User.objects.create(username=username, email=username, is_superuser = True, is_staff = True)
            instance = form.save(commit=False)
            instance.user = new_staff_user
            instance.save()
            return redirect('staffs')
    else:
        form = StaffsForm()
    
    context = {
        'form': form
    }
    
    return render(request, 'subisu/addstaff.html', context)




@login_required()
def view_emails(request):
    emails = EmailNotification.objects.all()
    context = {
        'emails' : emails
    }
    return render(request, 'subisu/emails.html', context)

@login_required()
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



@login_required()
def applications(request):
    
    applications = Applications.objects.all()
    context = {
        'applications' : applications
    }

    return render(request, 'subisu/applications.html', context)


@login_required()
def host_application_services(request, id):
    host = Hosts.objects.get(id  = id)
    applications = Applications.objects.filter(hostId = host)

    context = {
        'applications' : applications
    }
    
    return render(request, 'subisu/applications.html', context)


@login_required()
def poa(request):
    
    # activityId = models.ForeignKey(Activities, on_delete=models.CASCADE, verbose_name="Select Activity")
    # fieldEngineer = models.ManyToManyField(Staffs, blank=True, verbose_name="Select Field Engineers")
    # poaDetails = models.TextField(max_length=250, verbose_name="POA Details")
    # poaEntry = models.TimeField(auto_now_add=True, verbose_name="POA Entry")
    # sendEmail = models.BooleanField(default=True)
    # units = models.ManyToManyField(Units, blank=True, verbose_name="Send emails to Units")
    
    poa = Poa.objects.all()
    context = {
        'poas' : poa,
    }
    return render(request, 'subisu/poa.html', context)



@login_required()
def create_poa(request):
    activities = Activities.objects.filter(Q(status=ACTIVITY_STATUS[0][0]) | Q(status=ACTIVITY_STATUS[1][0]))
    field_engineers = Staffs.objects.filter(status=True)
    units = Units.objects.filter(status=True)
    
    if request.method == 'POST':
        activity_id = request.POST.get('activity_id')
        activity = Activities.objects.get(id=activity_id)
        selected_engineer_ids = request.POST.getlist('field_engineer[]')
        selected_field_engineers = Staffs.objects.filter(id__in=selected_engineer_ids)
        poa_details = request.POST.get('poa_details')
        send_email = 'send_email' in request.POST
        selected_unit_ids = request.POST.getlist('units[]')
        selected_units = Units.objects.filter(id__in=selected_unit_ids)
        entry_time = datetime.now().time()

        # Create POA object and save the data
        poa = Poa(activityId=activity, poaDetails=poa_details, sendEmail=send_email, poaEntry=entry_time)
        poa.save()
        poa.fieldEngineer.set(selected_field_engineers)
        poa.units.set(selected_units)
        
        # Redirect to the appropriate view after POA form submission
        return redirect('activities')  # Replace 'activities' with the desired view name
    
    context = {
        'activities': activities,
        'field_engineers': field_engineers,
        'units': units
    }

    return render(request, 'subisu/create_poa.html', context)



def error_404_view(request, exception):
    return HttpResponseNotFound(render(request, 'subisu/404.html'))

@login_required()
def departments(request):
    departments = Departments.objects.all()
    
    context = {
        'departments' : departments
    } 
    return render(request, 'subisu/departments.html', context)

@login_required()
def create_departments(request):
    if request.method == 'POST':
        form = DepartmentsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('departments')
    context = {
        'form' : DepartmentsForm
    }
    
    return render(request, 'subisu/add_departments.html', context)


@login_required()
def create_applications(request):
    if request.method == 'POST':
        form = ApplicationsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('applications')
    context = {
        'form' : ApplicationsForm
    }
    
    return render(request, 'subisu/add_applications.html', context)


