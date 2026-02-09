from django.urls import path
from User import views

app_name="User"

urlpatterns = [
    path('MyProfile/',views.myprofile,name="MyProfile"),
    path('editprofile/',views.editprofile,name="editprofile"),
    path('ChangePassword/',views.changepassword,name="changepassword"),
    path('HomePage/',views.homepageview,name="HomePage"),
    path('Complaint/',views.complaint,name="complaint"),
    path('delcomplaint/<int:did>',views.delcomplaint,name="delcomplaint"),

    path('viewservicecenter/',views.viewservicecenter,name="viewservicecenter"),
    path('AjaxLocation/',views.AjaxLocation,name="AjaxLocation"),
    path('servicebooking/<int:sid>',views.servicebooking,name="servicebooking"),
    path('myservicerequest/',views.myservice_request,name="myservicerequest"),
    

    path('AjaxVehicle/',views.AjaxVehicle,name="AjaxVehicle"),
    path('vehicle/',views.vehicle,name="vehicle"),
    path('worknote/<int:bid>',views.worknote,name="worknote"),
    path('payment/<int:bid>',views.payment,name="payment"),
    path('invoice/<int:bid>',views.invoice,name="invoice"),
    path('view_vehicle/',views.view_vehicle,name="myvehicle"),

    path('delvehicle/<int:did>',views.del_vehicle,name="delvehicle"),
    path('logout/',views.logout,name="logout"),

    path('breakdownassist/',views.breakdown_assist,name='breakdownassist'),
    path('BreakdownBooking/<int:sid>',views.breakdown_booking,name='BreakdownBooking'),
    path('breakdown_status/',views.breakdown_status,name="breakdown_status"),
    path("breakdown-payment/<int:bs_id>/",views.breakdown_payment,name="breakdown_payment"),
    path("breakdown-invoice/<int:bs_id>/",views.breakdown_invoice,name="breakdown_invoice"),
    path('feedback/<int:bid>',views.feedback,name="feedback"),


    
   
]