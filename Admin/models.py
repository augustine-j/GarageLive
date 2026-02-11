from django.db import models

# Create your models here.
class tbl_district(models.Model):
    district_name=models.CharField(max_length=50)

class tbl_category(models.Model):
    category_name=models.CharField(max_length=50)

class tbl_AdminRegistration(models.Model):
    admin_name=models.CharField(max_length=50)
    admin_email=models.CharField(max_length=50)
    admin_password=models.CharField(max_length=50)

class tbl_place(models.Model):
    place_name=models.CharField(max_length=50)
    district=models.ForeignKey(tbl_district,on_delete=models.CASCADE)

class tbl_department(models.Model):
    department_name=models.CharField(max_length=50)


class tbl_designation(models.Model):
    designation_name=models.CharField(max_length=50)


class tbl_employee(models.Model):
    employee_name=models.CharField(max_length=50)
    employee_gender=models.CharField(max_length=50)
    employee_contact=models.CharField(max_length=50)
    employee_doj=models.CharField(max_length=50)
    employee_salary=models.CharField(max_length=50)
    department=models.ForeignKey(tbl_department,on_delete=models.CASCADE)
    designation=models.ForeignKey(tbl_designation,on_delete=models.CASCADE)


class tbl_subcategory(models.Model):
    subcategory_name=models.CharField(max_length=50)
    category=models.ForeignKey(tbl_category,on_delete=models.CASCADE)
    

class tbl_servicetype(models.Model):
    servicetype_name=models.CharField(max_length=50)


class tbl_brand(models.Model):
    brand_name=models.CharField(max_length=50)

class tbl_model(models.Model):
    model_name=models.CharField(max_length=50)
    brand=models.ForeignKey(tbl_brand,on_delete=models.CASCADE)

    
class tbl_breakdown_servicetype(models.Model):
    servicetype_name = models.CharField(max_length=100)



class tbl_commision(models.Model):
    servicecenter=models.ForeignKey('Guest.tbl_servicecenter',on_delete=models.CASCADE)
    booking_type=models.IntegerField(choices=[(1,'Service Booking'),(2,'Breakdown Assistance')])
    booking_id=models.IntegerField()
    admin_commision=models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
