from django.contrib import admin
from django.urls import path
from monitor.views import camera_list,index,real
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('camera_list',camera_list),
    path('real',real),
]
