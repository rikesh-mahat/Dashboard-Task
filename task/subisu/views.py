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


@login_required()
def dashboard(request):
    
     # yoh tyo application dekhauna ko lagi hai
    applications = Applications.objects.all()
     
     
    # client services ko lagi
    client_services = ClientServices.objects.all()
    context = { 
        'applications' : applications,
        'client_services' : client_services
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
        
        user = User.objects.create(first_name = fname, last_name = lname, username = username, email = email)
        user.set_password(pass2)
        
        return redirect('admins')

    return render(request, 'subisu/signup.html')


def display_admin(request):
    admins = User.objects.filter(is_superuser  = True)
    context = {
        'admins' : admins
    }
    
    
    return render(request, 'subisu/admin.html', context)

def edit_admin(request, id):
    user = User.objects.get(id = id)
    return render(request, 'subisu/editadmin.html', {'user' : user})