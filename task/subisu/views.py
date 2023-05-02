from django.shortcuts import render, redirect
from Models.departments import Departments
# tyo Models ko application_access ko file bata ApplicationAccess bhanney import gareko
from Models.application_access import ApplicationAccess
from django.http import HttpResponse
from Models.applications import Applications
from Models.hosts import Hosts

def dashboard(request):
    # yesma mailey kei pani change garina hai
    
    return render(request, 'subisu/dashboard.html')



def hosts(request):
    
    hosts = Hosts.objects.all()
    context = {
        'hosts' : hosts
    }
    return render(request, 'subisu/host.html', context)


def add_host(request):
    if request.method == "POST":
        print("working")
    return render(request, 'subisu/addhost.html')