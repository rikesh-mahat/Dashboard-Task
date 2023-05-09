from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('hosts/', hosts, name='hosts'),
    path('add-host/', add_host, name='add_host'),
    path('delete-host/<int:id>/', delete_host, name='delete_host'),
    path('login/', login_user, name='login'),
    path('logout/', login_user, name='logout'),
    path('register/',register_user, name='register'),
    path('admins/', display_admin, name='admins'),
    path('edit-admin/<int:id>/', edit_admin, name='edit_admin'),
    path('activities/', activities, name='activities'),
    path('staffs/', display_staffs, name='staffs'),
    path('delete-staff/<int:id>/', delete_staff, name='delete_staff'),
    path('create-staff/', create_staff, name='create_staff')
]
