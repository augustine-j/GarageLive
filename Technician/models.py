from django.db import models
from User.models import *

# Create your models here.

class tbl_workedescription(models.Model):
    workedesc_content=models.CharField(max_length=50)
    booking=models.ForeignKey(tbl_booking,on_delete=models.CASCADE)
    
    
