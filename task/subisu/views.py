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


@login_required
def dashboard(request):
    # yesma mailey kei pani change garina hai
    # staff counts
    staff_counts = Staffs.objects.count()
    
    # department Counts
    department_counts = Departments.objects.count()
    
    # no of units
    client_count = ClientServices.objects.count()
    
    # no of applications
    applications_counts = Applications.objects.count()
     
     
    context = {
        'staffs' : staff_counts,
        'client_count' : client_count,
        'application' : applications_counts,
        'departments' : department_counts
    }
    return render(request, 'subisu/dashboard.html')


@login_required
def hosts(request):
    
    hosts = Hosts.objects.all()
    context = {
        'hosts' : hosts
    }
    return render(request, 'subisu/host.html', context)



@login_required
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