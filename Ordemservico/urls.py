from django.urls import path
from .views import OS_view, OsCreateView 

urlpatterns = [
 
    path('os/', OS_view, name='os.html'),
    path('os/create/', OsCreateView.as_view(), name='os_form'), 


]