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



# getting the user info like user, staff unit and department

def get_logged_user_info(request):
    if request.user.is_authenticated:
        
        # getting the logged in user informations
        user = request.user
        staff = Staffs.objects.get(user = user) # getting the user
        unit = staff.unitId # getting the unit of staff
        department = unit.departmentId # getting the department
        
        return [staff, unit, department]  # return the data in a list
        
        
        
        
        
# for filter emails

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


# dashboard view

@login_required()
def dashboard(request):
    
    
    host_counts = Hosts.objects.count()
    
    # getting the count of application, departments, unit and client services
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

    # getting today' date
    current_date = datetime.now().date()

    # getting the filter option from user side
    filter_option = request.GET.get('filter_option')
    
    # if start date is present and filter option is not none
    
    if start_date is None and filter_option is not None:
        if filter_option == "today":    # if filter option is set to today
            start_date = current_date - timedelta(days=0)
        elif filter_option == "this_week":  # if filter option is set to this week
            start_date = current_date - timedelta(days=6)  # set start date to 6 days ahead
        elif filter_option == "last_week": 
            start_date = current_date - timedelta(days=13) # set start date to 13 days ahead
            end_date = current_date - timedelta(days=7) # set end date to 7 days ahead
        else:
            start_date = datetime(current_date.year, current_date.month, 1).date()

    # Calculate the start and end dates for the previous five days
    start_date_default = current_date - timedelta(days=6)
    end_date_default = current_date  # default end date set to current date 

    
    start_date = start_date if start_date is not None else start_date_default  # get the start date or set to default
    end_date = end_date if end_date is not None else end_date_default # get the end date or set to default
     
    
    # if end date is backward than startdate return to same page with no changes
    if (end_date - start_date).days < 0:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
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

    
        
    # getting active and inactive client services
    client_services = ClientServices.objects.all()
    active_services = client_services.filter(serviceStatus=True).count()
    inactive_services = client_services.filter(serviceStatus=False).count()
    
    client_services_count = client_services.count()

   
    
    
    # passing data to client side
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
        'xlabel': json.dumps([str(day) for day in (start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1))]),  # for barchart
        'host_counts': host_counts,
        'activities_counts_json': activities_counts_json,
        'start_date_filter': start_date_filter,
        'end_date_filter': end_date_filter,
        'selected_option' : filter_option,
        'total_host' : Hosts.objects.all()
    }

    return render(request, 'subisu/dashboard.html', context)

# host view
@login_required()
def hosts(request):
    
    hosts = Hosts.objects.all()  # getting all the hosts
    context = {
        'hosts' : hosts
    }
    return render(request, 'subisu/host.html', context)


# add host views
@login_required()
def add_host(request):
    
    
    # check for post method
    if request.method == "POST":
        
        # getting the data from client side
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


# delete host view
@login_required()
def delete_host(request, id):
    
    # get the host by it's id
    host = Hosts.objects.get(id = id)
    host.delete() # delete the host
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




# login view
def login_user(request):
    
    # check for post method
    if request.method == "POST":
        
        # get the email and password
        email = request.POST.get('email')
        password = request.POST.get('password')

        # get email from session or set to none if not found
        session_username = request.session.get('email', None)
        
        # check for user with that email (user entered email)
        user = User.objects.filter(username=email).first()  # Retrieve the user
        
        # if user not found
        if not user:
            
            # notify the client about no user
            messages.error(request, "User doesn't exist")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # if the user's account is deactivated
        if not user.is_staff:
            
            # notify the user about account deactivation
            messages.warning(request, "Sorry, your account has been deactivated")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # if email was in session and session_username matches the client entered email 
        if session_username is not None and session_username == email:
            
            # get the number of attempts from session if available or set it to 0
            attempts = request.session.get('attempts', 0)
            
            # if user tries more than or equal to 4 invalid attempts
            if attempts >= 4:
                
                # disable the user and save it
                user.is_staff = False
                user.save()
                
                # notify the user about invalid attempts and account deactivation
                messages.error(request, "Sorry, your account has been disabled for incorrect attempts")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            # keep increasing the attempst value for invalid attempts
            attempts += 1
            request.session['attempts'] = attempts # update the attempts value in session
        else:
            request.session['attempts'] = 1  # Reset the attempts if a different user is logging in
            request.session['email'] = email

        # authenticate the user
        user = authenticate(username=email, password=password)

        # is user is authenticated 
        if user:
            
            # login the user
            login(request, user)
            request.session['attempts'] = 0  # Reset the attempts on successful login
            return redirect('dashboard')
        else:
            
            # else notify user about wrong credentials
            messages.warning(request, "Sorry, the credentials do not match")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'subisu/login.html')





# logout view
def logout_user(request):
    # thanks message + redirect to login page
    messages.info(request, "Thank you for using CMS. Sign in again")
    logout(request)
    return redirect('login')
    

# registering the user 
def register_user(request):
    
    # check if method is POST
    if request.method == "POST":
        # get the data from client side
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        email =  request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        
        
        # for checking if the user with that email exists
        user = User.objects.filter(username = username) 
        
        # if exists
        if user.exists():
            # notify the user
            messages.error(request, "Sorry the username is already taken")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        user = User.objects.filter(email = email)
        
        # check if password in less than 8 charcaters long
        if len(pass1) < 8:
            messages.warning(request, "Password should be minimum 8 Characters long")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        # check if password donot match
        if pass1 != pass2:
            messages.warning(request, "Password do not match")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        user = User.objects.create(first_name = fname, last_name = lname, username = username, email = email, is_superuser = True, is_staff=True)
        user.set_password(pass2)
        user.save()
        
        return redirect('admins')

    return render(request, 'subisu/signup.html')


# display admin view
@login_required()
def display_admin(request):
    
    # getting keyword from search 
    keyword = request.GET.get('keyword')
    admins = User.objects.filter(is_superuser=True)  # getting the admins

    # if keyword in not none
    if keyword:
        admins = admins.filter(
            Q(first_name__icontains=keyword) |
            Q(last_name__icontains=keyword) |
            Q(username__icontains=keyword) |
            Q(email__icontains=keyword)
        )
        
    # return the result
    context = {
        'admins': admins
    }
    
    return render(request, 'subisu/admin.html', context)



# edit admin view
@login_required()
def edit_admin(request, id):
    
    user = User.objects.get(id = id)
    return render(request, 'subisu/editadmin.html', {'user' : user})

# activities view
@login_required()
def activities(request):
    # getting the unit of logged in user
    unit = get_logged_user_info(request)[1]
    
    # only showing the activities of that unit
    activities = Activities.objects.filter(contact = unit).order_by('-created')
    
    # return date to client
    context = {
        'activities' : activities
    }
    return render(request, 'subisu/activities.html', context)



# create activities view
@login_required()
def create_acitivities(request):
    
    # if method is POST
    if request.method == "POST":
        context = {}
        
        # getting the activities form
        form = ActivitiesForm(request.POST)
        
        # if the form is valid
        if form.is_valid():
            # don't save the form yet
            activity = form.save(commit=False)
            
            # get the start time and end time from the form
            start_time = form.cleaned_data['startTime']
            end_time = form.cleaned_data['endTime']
            
            # check if start time and end time are not empty
            if start_time is None or end_time is None:
                
                # if empty notify the client
                messages.info(request,"Please choose a start time and end time")
                context['form'] = form
                return render(request, 'subisu/addactivities.html', context)
            
            # if end_time is behind of start time
            if end_time < start_time:
                
                # warn the user 
                messages.warning(request, "End time cannot be earlier than start time")
                context['form'] = form
                return render(request, 'subisu/addactivities.html', context)
            
            
            # get the comment from the form
            comment = form.cleaned_data['Comment']

            # getting the staff user name
            staff_name = request.user.username  # Default to username if staff attribute is not available

            # check if the user has attribute called staff
            if request.user.is_authenticated and hasattr(request.user, 'staff'):
                staff = request.user.staff
                activity.empId = staff
                # get the full name of staff
                staff_name = staff.firstName + " " + staff.middleName + " " +  staff.lastName if staff.middleName else  staff.firstName + " " +  staff.lastName
            staff_name = request.user.username
            
            # setting the contact of the user automatically
            if staff_name is not None:
                activity.contact = get_logged_user_info(request)[1]
            
            # finally save the form to database
            activity.save()
            
            # create the comment for that acitivity
            ActivityTable.objects.create(actId=activity, comment=comment, commentBy=staff_name)
            
            # if user ticks send email
            if 'send_email' in form.cleaned_data and form.cleaned_data['send_email']:
                
                # get the form data
                title = form.cleaned_data['title']
                location = form.cleaned_data['location']
                eta = form.cleaned_data['ETA']
                reason = form.cleaned_data['reason']
                impact = form.cleaned_data['impact']
                primary_email = form.cleaned_data['contact']
                other_emails = form.cleaned_data['otherEmails']
                email_list = process_emails(primary_email, other_emails)
               
                # send the email to the respective department
                msg = send_department_mail(title, eta, location, reason, impact, email_list)
                if msg:
                    # if msg == True notify the user about mail sent successfully
                    messages.info(request, "Mail sent successfully")
                else:
                    # notify user about mail could not be sent
                    messages.warning(request, "Sorry, Mail not sent due to an error")
            return redirect('create_poa')
        else:
            
            # if there are other error in the form
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


# edit activities view
@login_required()
def edit_activities(request, id):
    
    # get the activity id 
    activity = Activities.objects.get(id = id)
    
    # get the comment, start time and end time of the activity
    comments = ActivityTable.objects.filter(actId = activity)
    start_time = activity.startTime
    end_time = activity.endTime
    
    # if method is POST
    if request.method == "POST":
        # activity form with instance set to activity id
        form = ActivitiesForm(request.POST, instance=activity)
        
        
        # if the the form is valid
        if form.is_valid():
            
            # donot save the form yet
            activity = form.save(commit=False)
            
            # set the start time and end time
            activity.startTime = start_time
            activity.endTime = end_time
            
            # get new start tiem and end time
            new_start_time  = form.cleaned_data['startTime']
            new_end_time = form.cleaned_data['endTime']
            
            if start_time != new_start_time and new_start_time is not None:
                activity.startTime = new_start_time
            
            if end_time != new_end_time and new_end_time is not None:
                activity.endTime = new_end_time
            
            
            

            activity.save()
            time = f"{activity.startTime} - {activity.endTime}"
            
            
            # for comment
            comment = activity.Comment.strip()   # get the comment from the form
            last_comment_instance = ActivityTable.objects.filter(actId=activity).last() # get the last comment for the activity
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
                eta = form.cleaned_data['ETA']
                impact = form.cleaned_data['impact']
                primary_email = form.cleaned_data['contact']
                # retrieve otherEmails value from cleaned_data
                other_emails = form.cleaned_data['otherEmails']
                
        
                
                
                
                email_list = process_emails(primary_email, other_emails)
                
                
                msg = send_department_mail(title, eta, location, reason, impact, email_list)
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



# send activities mail view
def send_activities_mail(request, id):
    
    # get the activity by its id
    actvitiy = Activities.objects.get(id = id)
    
    # get the information from the activity
    title = actvitiy.title
    location = actvitiy.location
    benefits = actvitiy.benefits
    reason = actvitiy.reason
    impact = actvitiy.impact
    contact = actvitiy.contact
    other_emails = actvitiy.otherEmails
    time = f"{actvitiy.startTime} - {actvitiy.endTime}"
    email_list = process_emails(contact, other_emails)           
    
    # send the email 
    msg = send_department_mail(title,time,location, reason, benefits, impact, email_list)
    
    
    # wait fo the result
    if msg:
        # create the email log
        EmailNotification.objects.create(activityId = actvitiy, emailBody = " \n".join([title, location, benefits, reason, impact]))
        
        # notify the user
        messages.info(request, "Mail sent successfully")
        return redirect('activities')
    else:
        # notify the user
        messages.info(request, "Mail could not be sent! Error occurred")
        return redirect('activities')
    
    
    

# delete activity view
@login_required()
def delete_activity(request, id):
    
    # get the activity by its id
    activity = Activities.objects.get(id=id)
    activity.delete() # delete activity
    
    # notify the user
    messages.info(request, "Deleted the activity successfully")
    return redirect('activities')

# display staff view
@login_required()
def display_staffs(request):
    
    # get all the staffs of same unit
    unit =  get_logged_user_info(request)[1]
    staffs = Staffs.objects.filter(unitId = unit)
    
    # return the staffs to client side
    context = {
        'staffs' : staffs
    }
    return render(request, 'subisu/staffs.html', context)


# delete staff view
@login_required()
def delete_staff(request, id):
    # get the staff by id and delete it
    staff = Staffs.objects.get(id = id)
    staff.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



# create staff view
@login_required
def create_staff(request):
    
    # if method is post
    if request.method == 'POST':
        
        # get the staff form
        form = StaffsForm(request.POST)
        
        # if the form is valid
        if form.is_valid():
            # get the email from the form data
            username = form.cleaned_data['email']
            
            # check for user with that email
            users = User.objects.filter(Q(email=username) | Q(username=username))
            
            # if user already exists notify the client
            if users.exists():
                messages.warning(request, "Sorry, the email is already in use")
                return redirect('add_staff') 
            
            # if no user then create a staff and user assosciated to the staff
            new_staff_user = User.objects.create(username=username, email=username, is_superuser = True, is_staff = True)
            # set the password to 1234 and save the user
            new_staff_user.set_password('1234')
            new_staff_user.save()
            
            # get the instance of the staff and assign the user id to the staff and save it
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



# view email view
@login_required()
def view_emails(request):
    # get all the emails 
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


# application view
@login_required()
def applications(request):
    
    # get all the applications and fetch to client
    applications = Applications.objects.all()
    context = {
        'applications' : applications
    }

    return render(request, 'subisu/applications.html', context)

# host application services
@login_required()
def host_application_services(request, id):
    
    # get the host by its id and show all its applications
    host = Hosts.objects.get(id  = id)
    applications = Applications.objects.filter(hostId = host)

    context = {
        'applications' : applications
    }
    
    return render(request, 'subisu/applications.html', context)


# poa view
@login_required()
def poa(request):
    
    # get all the poa and fetch to client
    poa = Poa.objects.all()
    context = {
        'poas' : poa,
    }
    return render(request, 'subisu/poa.html', context)


# create poa view
@login_required()
def create_poa(request):
    
    # get the unit of the logged in staff
    unit = get_logged_user_info(request)[1]\
    
    # get all the activities of same unit
    activities = Activities.objects.filter(Q(status=ACTIVITY_STATUS[0][0]) | Q(status=ACTIVITY_STATUS[1][0]), contact = unit)
    
    # get all the staffs of same unit
    field_engineers = Staffs.objects.filter(status = True, unitId = unit)
    units = Units.objects.filter(status=True)
    
    
    # if the method is POST
    if request.method == 'POST':
        
        # get the information form the client side
        activity_id = request.POST.get('activity_id')
        activity = Activities.objects.get(id=activity_id)
        selected_engineer_ids = request.POST.getlist('field_engineer[]')
        selected_field_engineers = Staffs.objects.filter(id__in=selected_engineer_ids)
        poa_details = request.POST.get('poa_details')
        send_email = 'send_email' in request.POST
        selected_unit_ids = request.POST.getlist('units[]')
        selected_units = Units.objects.filter(id__in=selected_unit_ids)
        
        # automatically set the logtime
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


# error 404 view
def error_404_view(request, exception):
    return HttpResponseNotFound(render(request, 'subisu/404.html'))



# department view
@login_required()
def departments(request):
    
    # get all the departments
    departments = Departments.objects.all()
    
    context = {
        'departments' : departments
    } 
    return render(request, 'subisu/departments.html', context)

# create department view
@login_required()
def create_departments(request):
    # if method is POST
    if request.method == 'POST':
        
        # get the form data
        form = DepartmentsForm(request.POST)
        
        # check for validity
        if form.is_valid():
            
            # if valid save the form data in database
            form.save()
            return redirect('departments')
    context = {
        'form' : DepartmentsForm
    }
    
    return render(request, 'subisu/add_departments.html', context)

# createa application view
@login_required()
def create_applications(request):
    # if method is post
    if request.method == 'POST':
        
        # application form data
        form = ApplicationsForm(request.POST)
        
        # validity of form
        if form.is_valid():
            
            # save the form data in database
            form.save()
            return redirect('applications')
    context = {
        'form' : ApplicationsForm
    }
    
    return render(request, 'subisu/add_applications.html', context)


