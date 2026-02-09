from django.db import models
from Guest.models import *
from Admin.models import *
from ServiceCenter.models import *



# Create your models here.

class tbl_complaint(models.Model):
    complaint_title=models.CharField(max_length=50)
    complaint_content=models.CharField(max_length=50)
    complaint_date=models.DateField(auto_now_add=True)
    complaint_reply=models.CharField(max_length=50,null=True)
    complaint_status=models.IntegerField(default=0)
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)




class tbl_vehicle(models.Model):
    vehicle_number=models.CharField(max_length=50)
    vehicle_year=models.CharField(max_length=50)
    vehicle_photo=models.FileField(upload_to='Assets/VehicleDocs/')
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
    model=models.ForeignKey(tbl_model,on_delete=models.CASCADE)

class tbl_booking(models.Model):
    booking_date=models.DateField(auto_now_add=True)
    booking_todate=models.DateField()
    
    booking_status=models.IntegerField(default=0)
    booking_complaints=models.CharField(max_length=50)
            
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
    servicecenter=models.ForeignKey(tbl_servicecenter,on_delete=models.CASCADE)
    vehicle=models.ForeignKey(tbl_vehicle,on_delete=models.CASCADE)
    technician=models.ForeignKey(tbl_technician,on_delete=models.CASCADE,null=True)



class tbl_booking_services(models.Model):
    booking=models.ForeignKey(tbl_booking,on_delete=models.CASCADE)
    servicecenter_services=models.ForeignKey(tbl_servicecenterservices,on_delete=models.CASCADE)
    base_amount=models.DecimalField(max_digits=10, decimal_places=2)
    labour_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True)
    parts_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)





class tbl_breakdownassist(models.Model):
    breakdown_date=models.DateField(auto_now_add=True)
    breakdown_complaint=models.CharField(max_length=50)
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
    vehicle=models.ForeignKey(tbl_vehicle,on_delete=models.CASCADE)
    servicecenter=models.ForeignKey(tbl_servicecenter,on_delete=models.CASCADE)
    technician=models.ForeignKey(tbl_technician,on_delete=models.CASCADE,null=True)
    breakdown_status=models.IntegerField(default=0)



class tbl_breakdown_booking_services(models.Model):
    booking = models.ForeignKey(tbl_breakdownassist,on_delete=models.CASCADE)

    servicecenter_breakdown_service = models.ForeignKey(tbl_servicecenter_breakdown_services,on_delete=models.CASCADE)
    progress_step = models.IntegerField(default=0)
    base_amount = models.DecimalField(max_digits=10,decimal_places=2)
    extra_charge = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    final_amount = models.DecimalField(max_digits=10,decimal_places=2)
    billing_status = models.BooleanField(default=False)
    payment_status = models.BooleanField(default=False)


    
class tbl_feedback(models.Model):
    RATING_CHOICES = (
        (1, 'Very Bad'),
        (2, 'Bad'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent'),
    )

    feedback_content = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    feedback_date = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(tbl_user,on_delete=models.CASCADE,related_name='feedbacks')
    servicecenter = models.ForeignKey(tbl_servicecenter,on_delete=models.CASCADE,related_name='feedbacks')
    booking = models.OneToOneField(tbl_booking,on_delete=models.CASCADE,related_name='feedback')

    def __str__(self):
        return f"{self.servicecenter} - {self.rating}⭐"
