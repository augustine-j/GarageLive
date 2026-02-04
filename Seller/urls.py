from django.urls import path
from Seller import views

app_name="Seller"

urlpatterns = [
    path('HomePage/',views.homepage,name="HomePage"),
    path('Profile/',views.profile,name="profile"),
    path('editprofile/',views.editprofile,name="editprofile"),
    path('changepassword/',views.changepassword,name="changepassword")

]