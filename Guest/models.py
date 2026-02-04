from django.db import models
from Admin.models import *

# Create your models here.
class tbl_user(models.Model):
    user_name=models.CharField(max_length=50)
    user_gender=models.CharField(max_length=50)
    contact_number=models.CharField(max_length=50)
    user_email=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    address=models.CharField(max_length=50)
    image=models.FileField(upload_to='Assets/UserDocs/')
    user_status=models.IntegerField(default=0)


class tbl_seller(models.Model):
    user_name=models.CharField(max_length=50)
    contact_number=models.CharField(max_length=50)
    user_email=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    estd_date=models.CharField(max_length=50)
    license_number=models.CharField(max_length=50)
    owner_name=models.CharField(max_length=50)
    license_proof=models.FileField(upload_to='Assets/SellerDocs/')
    owner_proof=models.FileField(upload_to='Assests/SellerDocs/')
    seller_status=models.IntegerField(default=0)




class tbl_servicecenter(models.Model):
    servicecenter_name=models.CharField(max_length=50)
    servicecenter_email=models.CharField(max_length=50)
    servicecenter_contact=models.CharField(max_length=50)
    servicecenter_address=models.CharField(max_length=50)
    servicecenter_logo=models.FileField(upload_to='Assets/ServicecenterDocs/')
    servicecenter_license=models.FileField(upload_to='Assets/ServicecenterDocs/')
    servicecenter_password=models.CharField(max_length=50)
    servicecenter_status=models.IntegerField(default=0)
    servicecenter_regdate=models.DateField(auto_now_add=True)
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
