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
    path('edit-admin/<int:id>/', edit_admin, name='edit_admin')
]
