
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('subisu.urls'))
]

handler404 = 'subisu.views.error_404_view'