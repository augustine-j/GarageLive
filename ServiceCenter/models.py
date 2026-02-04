from django.db import models
from Guest.models import *
from Admin.models import *

# Create your models here.

class tbl_technician(models.Model):
    technician_name=models.CharField(max_length=50)
    technician_email=models.CharField(max_length=50)
    technician_contact=models.CharField(max_length=50)
    technician_photo=models.FileField(upload_to='Assets/TechnicianDocs/')
    technician_password=models.CharField(max_length=50)
    servicecenter=models.ForeignKey(tbl_servicecenter,on_delete=models.CASCADE)
    
    



class tbl_servicecenterservices(models.Model):
    servicetype=models.ForeignKey(tbl_servicetype,on_delete=models.CASCADE)
    servicecenter=models.ForeignKey(tbl_servicecenter,on_delete=models.CASCADE)
    base_amount=models.DecimalField(max_digits=10, decimal_places=2)

    

class tbl_servicecenter_breakdown_services(models.Model):
    servicecenter = models.ForeignKey(tbl_servicecenter,on_delete=models.CASCADE)
    servicetype = models.ForeignKey(tbl_breakdown_servicetype,on_delete=models.CASCADE)
    base_amount = models.DecimalField(max_digits=10, decimal_places=2)
