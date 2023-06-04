from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('', login_required(dashboard), name='dashboard'),
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
    path('create-staff/', create_staff, name='create_staff'),
    path('add-activities/', create_acitivities, name ='create_activities'),
    path('delete-activity/<int:id>/',delete_activity, name= 'delete_activity'),
    path('edit-activity/<int:id>/', edit_activities, name='edit_activity'),
    path('send-activities-mail/<int:id>/', send_activities_mail, name='activities_mail'),
    path('email/', view_emails, name='emails'),
    path('profile/', user_profile, name='profile'),
    path('applications/', applications, name='applications'),
    path('application/<int:id>/', host_application_services , name="application")
]
