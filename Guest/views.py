from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *
from ServiceCenter.models import *
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

def newuser(request):
    
    placedata=tbl_place.objects.all()
    districtdata=tbl_district.objects.all()
    if request.method=="POST":
        name=request.POST.get("txt_name")
        gender=request.POST.get("gender")
        contact=request.POST.get("txt_contact")
        email=request.POST.get("txt_email")
        password=request.POST.get("txt_password")
        place=tbl_place.objects.get(id=request.POST.get("sel_place"))
        address=request.POST.get("txt_address")
        image=request.FILES.get("image")

        usercount=tbl_user.objects.filter(user_email=email).count()
        if usercount>0:
            return render(request,"Guest/NewUser.html",{'msg':"User already exists with this email"})
        else:

            userdata=tbl_user.objects.create(user_name=name,user_gender=gender,contact_number=contact,user_email=email,password=password,
            place=place,address=address,image=image)
            email=userdata.user_email
            subject = "Welcome to GarageLive 🚗"
            message = (
                "Dear User,\n\n"
                "Welcome to GarageLive!\n\n"
                "Your account has been successfully verified and approved by our admin team. "
                "You can now log in and start using all the features of GarageLive, including:\n\n"
                "• Booking vehicle services\n"
                "• Tracking service status\n"
                "• Managing your vehicle details\n"
                "• Easy communication with service centers\n\n"
                "If you face any issues or have questions, feel free to contact our support team.\n\n"
                "We’re excited to have you onboard!\n\n"
                "Warm regards,\n"
                "GarageLive Team"
            )

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return render(request,"Guest/NewUser.html",{'msg':"User Registered"})
    else:
        return render(request,"Guest/NewUser.html",{'placedata':placedata,'districtdata':districtdata})


def AjaxPlace(request):
    districtid=request.GET.get('did')
    placedata=tbl_place.objects.filter(district=districtid)
    return render(request,'Guest/Ajaxplace.html',{'placedata':placedata})


def login(request):
    if request.method=="POST":
        email=request.POST.get("txt_email")
        password=request.POST.get("txt_password")
        
        usercount=tbl_user.objects.filter(user_email=email,password=password).count()
        admincount=tbl_AdminRegistration.objects.filter(admin_email=email,admin_password=password).count()
        
        
        
        centercount=tbl_servicecenter.objects.filter(servicecenter_email=email,servicecenter_password=password,servicecenter_status=1).count()
        techniciancount=tbl_technician.objects.filter(technician_email=email,technician_password=password).count()

        if usercount>0:
            userdata=tbl_user.objects.get(user_email=email,password=password)
            request.session['uid']=userdata.id
            return redirect("User:HomePage")
        

        elif admincount>0:
            admindata=tbl_AdminRegistration.objects.get(admin_email=email,admin_password=password)
            request.session['aid']=admindata.id
            return redirect("Admin:AdminHome")
        

        

        elif centercount>0:
            centerdata=tbl_servicecenter.objects.get(servicecenter_email=email,servicecenter_password=password)
            request.session['cid']=centerdata.id
            return redirect("ServiceCenter:HomePage")

        elif techniciancount>0:
            techniciandata=tbl_technician.objects.get(technician_email=email,technician_password=password)
            request.session['tid']=techniciandata.id
            return redirect("Technician:HomePage")
        else:
            return render(request,"Guest/Login.html",{'msg':"Invalid Login"})
        
    else:
        return render(request,'Guest/Login.html')




    
        

        


    
    


def servicecenter(request):
    placedata=tbl_place.objects.all()
    districtdata=tbl_district.objects.all()

    if request.method=="POST":
        name=request.POST.get("txt_name")
        email=request.POST.get("txt_email")
        number=request.POST.get("txt_contact")
        address=request.POST.get("txt_address")
        logo=request.FILES.get("file_logo")
        license_proof=request.FILES.get("file_license")
        password=request.POST.get("txt_password")
        place=tbl_place.objects.get(id=request.POST.get("sel_place"))

        servicecentercount=tbl_servicecenter.objects.filter(servicecenter_email=email).count()
        if servicecentercount>0:
            return render(request,"Guest/ServiceCenterReg.html",{'msg':"center with email already exists"})
        else:


            tbl_servicecenter.objects.create(servicecenter_name=name,servicecenter_email=email,servicecenter_contact=number,
            servicecenter_address=address,servicecenter_logo=logo,servicecenter_license=license_proof,servicecenter_password=password,
            place=place)
            return render(request,"Guest/ServiceCenterReg.html",{'msg':"Center Registered,wait for admin approval",'placedata':placedata,'districtdata':districtdata})
    else:
        return render(request,"Guest/ServiceCenterReg.html",{'placedata':placedata,'districtdata':districtdata})




def indexpage(request):
    return render(request,"Guest/index.html")