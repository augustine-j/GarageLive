from django.urls import path
from Guest import views
app_name="Guest"

urlpatterns = [
    path('NewUser/',views.newuser,name="NewUser"),
    path('AjaxPlace/',views.AjaxPlace,name='AjaxPlace'),
    path('Login/',views.login,name='Login'),
    

    path('Servicecentereg/',views.servicecenter,name='servicecenter'),
    

    path('indexpage/',views.indexpage,name="indexpage"),
    path('',views.indexpage,name="indexpage"),

]