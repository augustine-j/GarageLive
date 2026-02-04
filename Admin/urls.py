from django.urls import path,include
from Admin import views

app_name="Admin"

urlpatterns = [
    path('District/',views.district,name="District"),
    path('Category/',views.category,name="Category"),
    path('AdminRegistration/',views.AdminRegistration,name="AdminRegistration"),
    path('deldistrict/<int:did>',views.deldistrict,name="deldistrict"),
    path('delcategory/<int:did>',views.delcategory,name="delcategory"),
    path('delregistration/<int:did>',views.delregistration,name="delregistration"),
    path('editdistrict/<int:eid>',views.editdistrict,name="editdistrict"),
    path('editcategory/<int:eid>',views.editcategory,name="editcategory"),
    path('editregistration/<int:eid>',views.editregistration,name="editregistration"),
    path('Place/',views.place,name="Place"),
    path('editplace/<int:eid>',views.editplace,name="editplace"),
    path('delplace/<int:did>',views.delplace,name="delplace"),

    path('Department/',views.department,name="Department"),
    path('editdepartment/<int:eid>',views.editdepartment,name="editdepartment"),
    path('deldepartment/<int:did>',views.deldepartment,name="deldepartment"),

    path('Designation',views.designation,name="Designation"),
    path('editdesignation/<int:eid>',views.editdesignation,name="editdesignation"),
    path('deldesignation/<int:did>',views.deldesignation,name="deldesignation"),
    
    path('Employee',views.employee,name="Employee"),
    path('editemployee/<int:eid>',views.editemployee,name="editemployee"),
    path('delemployee/<int:did>',views.delemployee,name="delemployee"),
    
    path('Subcategory',views.subcategory,name="Subcategory"),
    path('editsubcategory/<int:eid>',views.editsubcategory,name="editsubcategory"),
    path('delsubcategory/<int:did>',views.delsubcategory,name="delsubcategory"),
    
    path('SellerView/',views.sellerview,name="SellerView"),
    path('UserList/',views.userview,name="UserView"),
    path('acceptseller/<int:aid>',views.acceptseller,name="acceptseller"),
    path('rejectseller/<int:rid>',views.rejectseller,name="rejectseller"),
    path('acceptuser/<int:aid>',views.acceptuser,name="acceptuser"),
    path('rejectuser/<int:rid>',views.rejectuser,name="rejectuser"),
    
    path('AdminHome/',views.adminhome,name="AdminHome"),

    path('complaint/',views.complaint,name="complaint"),
    path('reply/<int:cid>',views.reply,name="reply"),

    path('centerverlist/',views.centerlist,name='centerlist'),
    path('acceptcenter/<int:aid>',views.acceptcenter,name='acceptcenter'),
    path('rejectcenter/<int:rid>',views.rejectcenter,name='rejectcenter'),

    path('servicetype/',views.servicetype,name="servicetype"),
    path('delservicetype/<int:did>',views.delservicetype,name='delservicetype'),
    path('editservicetype/<int:eid>',views.editservicetype,name='editservicetype'),

    path('Brand/',views.brand,name="brand"),
    path('delbrand/<int:did>',views.delbrand,name="delbrand"),
    path('editbrand/<int:eid>',views.editbrand,name="editbrand"),

    path('model/',views.brand_model,name="model"),
    path('delmodel/<int:did>',views.delmodel,name="delmodel"),
    path('editmodel/<int:eid>',views.editmodel,name="editmodel"),

    path('logout/',views.logout,name="logout"),


    path("breakdown-servicetype/", views.breakdown_servicetype, name="breakdown_servicetype"),
    path("breakdown-servicetype/edit/<int:eid>/", views.edit_breakdown_servicetype, name="edit_breakdown_servicetype"),
    path("breakdown-servicetype/delete/<int:did>/", views.del_breakdown_servicetype, name="del_breakdown_servicetype"),

    
]