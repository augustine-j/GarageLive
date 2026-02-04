from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *
from ServiceCenter.models import *


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

            tbl_user.objects.create(user_name=name,user_gender=gender,contact_number=contact,user_email=email,password=password,
            place=place,address=address,image=image)
            return render(request,"Guest/NewUser.html",{'msg':"record inserted"})
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
        
        usercount=tbl_user.objects.filter(user_email=email,password=password,user_status=1).count()
        admincount=tbl_AdminRegistration.objects.filter(admin_email=email,admin_password=password).count()
        sellercount=tbl_seller.objects.filter(user_email=email,password=password).count()
        
        
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
        

        elif sellercount>0:
            sellerdata=tbl_seller.objects.get(user_email=email,password=password)
            request.session['sid']=sellerdata.id
            return redirect("Seller:HomePage")

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




    
        

        

def newseller(request):
    placedata=tbl_place.objects.all()
    districtdata=tbl_district.objects.all()
    if request.method=="POST":
        name=request.POST.get("txt_name")
        contact=request.POST.get("txt_number")
        email=request.POST.get("txt_email")
        password=request.POST.get("txt_password")
        place=tbl_place.objects.get(id=request.POST.get("sel_place"))
        estd_date=request.POST.get("estd_date")
        license_number=request.POST.get("txt_license")
        owner_name=request.POST.get("txt_owner")
        license_proof=request.FILES.get("license")
        owner_proof=request.FILES.get("owner")
        tbl_seller.objects.create(user_name=name,contact_number=contact,user_email=email,password=password,place=place,estd_date=estd_date,
        license_number=license_number,owner_name=owner_name,license_proof=license_proof,owner_proof=owner_proof)
        return render(request,"Guest/NewSeller.html",{'msg':"Record inserted"})
    else:
        return render(request,"Guest/NewSeller.html",{'placedata':placedata,'districtdata':districtdata})
    
    


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
            return render(request,"Guest/ServiceCenterReg.html",{'msg':"Center Registered"})
    else:
        return render(request,"Guest/ServiceCenterReg.html",{'placedata':placedata,'districtdata':districtdata})




def indexpage(request):
    return render(request,"Guest/index.html")