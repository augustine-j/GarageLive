from django.urls import path
from Technician import views

app_name="Technician"

urlpatterns = [
     path('HomePage/',views.homepage,name="HomePage"),
     path('profile/',views.profile,name="profile"),
     path('editprofile/',views.editprofile,name="editprofile"),
     path('changepassword/',views.changepassword,name="changepassword"),
     path('assignedjobs/',views.assigned_jobs,name="assigned_jobs"),
     path('startwork/<int:sid>',views.startwork,name="startwork"),
     path('startdiagnosis/<int:did>',views.start_diagnosis,name="start_diagnosis"),
     path('diagnosis_completed/<int:cdid>',views.diagnosis_completed,name="diagnosis_completed"),
     path('repair_progress/<int:rid>',views.repair_progress,name="repair_progress"),
     path('parts_replaced/<int:pid>',views.parts_replaced,name="parts_replaced"),
     path('testing_QA/<int:tid>',views.testing_QA,name="testing_QA"),
     path('service_completed/<int:sid>',views.service_completed,name="service_completed"),
     path('out_delivery/<int:did>',views.out_delivery,name="out_delivery"),
     # path('delivered/<int:did>',views.delivered,name="delivered"),
     path('workdescription/<int:bid>',views.workdescription,name="workdescription"),
     path('logout/',views.logout,name="logout"),

     path('update-service-cost/<int:booking_id>/', views.update_service_cost, name='update_service_cost'),

     path('breakdown-jobs/',views.breakdown_jobs,name='breakdown_jobs'),
      
     path('breakdown-step/<int:sid>/', views.update_breakdown_step, name='update_breakdown_step'),
     path('update_breakdown_charge/<int:bs_id>',views.update_breakdown_charge,name="update_breakdown_charge"),

    




     
]