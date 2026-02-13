from django.urls import path
from ServiceCenter import views

app_name="ServiceCenter"

urlpatterns = [
     path('HomePage/',views.homepage,name="HomePage"),
     path('Profile/',views.profile,name="profile"),
     path('editprofile/',views.editprofile,name="editprofile"),
     path('changepassword/',views.changepassword,name="changepassword"),
     path('technician/',views.technician,name="technician"),
     path('deltechnician/<int:did>',views.deltechnician,name="deltechnician"),

     path('myservices/',views.myservices,name="myservices"),
     path('editmy_services/<int:sid>',views.editmy_services,name="editmy_services"),
     path('delmyservices/<int:did>',views.delmyservices,name="delmyservices"),

     path('service_request/',views.service_requests,name="service_request"),
     path('acceptrequest/<int:aid>',views.acceptrequest,name="acceptrequest"),
     path('rejectrequest/<int:rid>',views.rejectrequest,name="rejectrequest"),

     path('assign_technician/<int:bid>',views.assign_technician,name="assign_technician"),
     path('assignjob/<int:tid>/<int:bid>',views.assignjob,name="assignjob"),
     path('generate_bill/<int:bid>',views.generate_bill,name="generate_bill"),
     path('logout/',views.logout,name="logout"),

     path('breakdownrequest/',views.breakdown_requests,name="breakdownrequest"),
     path('acceptbreakdown/<int:aid>',views.acceptbreakdown,name="acceptbreakdown"),
     path('rejectbreakdown/<int:rid>',views.rejectbreakdown,name="rejectbreakdown"),
     path('breakdown_technician/<int:btid>',views.breakdown_technician,name="breakdown_technician"),
     path('assign_breakdown/<int:tid>/<int:btid>',views.assign_breakdown,name="assign_breakdown"),

     path('my-breakdown-services/', views.my_breakdown_services, name='my_breakdown_services'),

     path('edit-breakdown-service/<int:sid>/',views.edit_breakdown_service,name='edit_breakdown_service'),

     path('delete-breakdown-service/<int:did>/',views.delete_breakdown_service,name='delete_breakdown_service'),
     path('view_feedback/',views.view_feedback,name="view_feedback"),

     path('chart-homepage/', views.chart_homepage, name='chart_homepage'),
     path('weekly-income-chart/', views.weekly_income_chart, name='weekly_income_chart'),
    

     
     


     


     




]