from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *
from User.models import *

from django.utils import timezone
from datetime import date
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
def district(request):
     if 'aid' not in request.session:
      return redirect("Guest:Login")
     else:
        districtdata=tbl_district.objects.all()
        greeting=tbl_AdminRegistration.objects.get(id=request.session['aid'])
        if request.method=="POST":
            district=request.POST.get("txt_name")
            distrcitcount=tbl_district.objects.filter(district_name=district).count()
            if distrcitcount>0:
                return render(request,"Admin/District.html",{'msg':"District already exists"})
            else:

                tbl_district.objects.create(district_name=district)
                return render(request,"Admin/District.html",{'msg':"Data inserted"})
        
        else:

            return render(request,"Admin/District.html",{'districtdata':districtdata,'greeting':greeting})


def category(request):
    categorydata=tbl_category.objects.all()
    if request.method=="POST":
        category=request.POST.get("txt_name")
        tbl_category.objects.create(category_name=category)
        return render(request,"Admin/Category.html",{'msg':"Category inserted"})
    else:
        return render(request,"Admin/Category.html",{'categorydata':categorydata})


def AdminRegistration(request):
    regdata=tbl_AdminRegistration.objects.all()
    if request.method=="POST":
        name=request.POST.get("txt_name")
        email=request.POST.get("txt_email")
        password=request.POST.get("txt_password")
        admincount=tbl_AdminRegistration.objects.filter(admin_email=email).count()
        if admincount>0:
            return render(request,"Admin/AdminRegistration.html",{'msg':"Email already exists"})
        else:


            tbl_AdminRegistration.objects.create(admin_name=name,admin_email=email,admin_password=password)
            return render(request,"Admin/AdminRegistration.html",{'msg':"Records inserted"})
    else:
        return render(request,"Admin/AdminRegistration.html",{'regdata':regdata})


def deldistrict(request,did):
    tbl_district.objects.get(id=did).delete()
    return redirect("Admin:District")

def delcategory(request,did):
    tbl_category.objects.get(id=did).delete()
    return redirect("Admin:Category")

def delregistration(request,did):
    tbl_AdminRegistration.objects.get(id=did).delete()
    return redirect("Admin:AdminRegistration")

def editdistrict(request,eid):
    editdata=tbl_district.objects.get(id=eid)
    
    if request.method=="POST":
        district=request.POST.get("txt_name")
        editdata.district_name=district
        editdata.save()
        return redirect("Admin:District")
    else:
        return render(request,"Admin/District.html",{'editdata':editdata})


def editcategory(request,eid):
    editdata=tbl_category.objects.get(id=eid)
    if request.method=="POST":
        category=request.POST.get("txt_name")
        editdata.category_name=category
        editdata.save()
        return redirect("Admin:Category")
    else:
        return render(request,"Admin/Category.html",{'editdata':editdata})
    

def editregistration(request,eid):
    editdata=tbl_AdminRegistration.objects.get(id=eid)
    if request.method=="POST":
        name=request.POST.get("txt_name")
        email=request.POST.get("txt_email")
        password=request.POST.get("txt_password")
        editdata.admin_name=name
        editdata.admin_email=email
        editdata.admin_password=password
        editdata.save()
        return redirect("Admin:AdminRegistration")
    else:
        return render(request,"Admin/AdminRegistration.html",{'editdata':editdata})


def place(request):
     if 'aid' not in request.session:
      return redirect("Guest:Login")
     else:

        districtdata=tbl_district.objects.all()
        placedata=tbl_place.objects.all()
        greeting=tbl_AdminRegistration.objects.get(id=request.session['aid'])
        if request.method=="POST":
            district=tbl_district.objects.get(id=request.POST.get("select_district"))
            place=request.POST.get("txt_place")
            placecount=tbl_place.objects.filter(place_name=place).count()
            if placecount>0:
                return render(request,"Admin/Place.html",{'msg':"Place already exists"})
            else:
                tbl_place.objects.create(place_name=place,district=district)
                return render(request,"Admin/Place.html",{'msg':"Data inserted"})
        else:
            return render(request,"Admin/Place.html",{'districtdata':districtdata,'placedata':placedata,'greeting':greeting})

def editplace(request,eid):
    districtdata=tbl_district.objects.all()
    editplace=tbl_place.objects.get(id=eid)
    if request.method=="POST":
        district=tbl_district.objects.get(id=request.POST.get("select_district"))
        place=request.POST.get("txt_place")
        editplace.place_name=place
        editplace.district=district
        editplace.save()
        return redirect("Admin:Place")
    else:
        return render(request,"Admin/Place.html",{'editplace':editplace,'districtdata':districtdata})


def delplace(request,did):
    tbl_place.objects.get(id=did).delete()
    return redirect("Admin:Place")


def department(request):
    deptdata=tbl_department.objects.all()
    if request.method=="POST":
        department=request.POST.get("dept_name")
        tbl_department.objects.create(department_name=department)
        return render(request,"Admin/Department.html",{'msg':"Data inserted"})
    else:
        return render(request,"Admin/Department.html",{'deptdata':deptdata})
    
def editdepartment(request,eid):
    editdept=tbl_department.objects.get(id=eid)
    if request.method=="POST":
        dept=request.POST.get("dept_name")
        editdept.department_name=dept
        editdept.save()
        return redirect("Admin:Department")
    else:
        return render(request,"Admin/Department.html",{'editdept':editdept})

def deldepartment(request,did):
    tbl_department.objects.get(id=did).delete()
    return redirect("Admin:Department")

def designation(request):
    desidata=tbl_designation.objects.all()
    if request.method=="POST":
        designation=request.POST.get("txt_designation")
        tbl_designation.objects.create(designation_name=designation)
        return render(request,"Admin/Designation.html",{'msg':"Data inserted"})
    else:
        return render(request,"Admin/Designation.html",{'desidata':desidata})


def editdesignation(request,eid):
    editdesi=tbl_designation.objects.get(id=eid)

    if request.method=="POST":
        designation=request.POST.get("txt_designation")
        editdesi.designation_name=designation
        editdesi.save()
        return redirect("Admin:Designation")
    else:
        return render(request,"Admin/Designation.html",{'editdesi':editdesi})


def deldesignation(request,did):
    tbl_designation.objects.get(id=did).delete()
    return redirect("Admin:Designation")



def employee(request):
    deptdat=tbl_department.objects.all()
    desidata=tbl_designation.objects.all()
    empdata=tbl_employee.objects.all()
    if request.method=="POST":
        name=request.POST.get("txt_name")
        gender=request.POST.get("gender")
        contact=request.POST.get("txt_num")
        doj=request.POST.get("txt_doj")
        department=tbl_department.objects.get(id=request.POST.get("select_department"))
        designation=tbl_designation.objects.get(id=request.POST.get("select_designation"))
        salary=request.POST.get("txt_salary")
        tbl_employee.objects.create(employee_name=name,employee_gender=gender,employee_contact=contact,employee_doj=doj,
        department=department,designation=designation,employee_salary=salary)
        return render(request,"Admin/Employee.html",{'msg':"Data inserted"})

    else:
        return render(request,"Admin/Employee.html",{'deptdata':deptdat,'desidata':desidata,'empdata':empdata})


def editemployee(request,eid):
    deptdata=tbl_department.objects.all()
    desidata=tbl_designation.objects.all()
    editemp=tbl_employee.objects.get(id=eid)
    if request.method=="POST":
        department=tbl_department.objects.get(id=request.POST.get("select_department"))
        designation=tbl_designation.objects.get(id=request.POST.get("select_designation"))
        name=request.POST.get("txt_name")
        gender=request.POST.get("gender")
        contact=request.POST.get("txt_num")
        doj=request.POST.get("txt_doj")
        salary=request.POST.get("txt_salary")
        editemp.employee_name=name
        editemp.employee_gender=gender
        editemp.employee_contact=contact
        editemp.employee_doj=doj
        editemp.employee_salary=salary
        editemp.department=department
        editemp.designation=designation
        editemp.save()
        return redirect("Admin:Employee")
    else:
        return render(request,"Admin/Employee.html",{'deptdata':deptdata,'desidata':desidata,'editemp':editemp})


def delemployee(request,did):
    tbl_employee.objects.get(id=did).delete()
    return redirect("Admin:Employee")



def subcategory(request):
    categorydata=tbl_category.objects.all()
    subcategory=tbl_subcategory.objects.all()
    if request.method=="POST":
        category=tbl_category.objects.get(id=request.POST.get("select_category"))
        subcategory=request.POST.get("txt_sub")
        tbl_subcategory.objects.create(subcategory_name=subcategory,category=category)

        return render(request,"Admin/Subcategory.html",{'msg':"data inserted"})
    else:
        return render(request,"Admin/Subcategory.html",{'categorydata':categorydata,'subcategory':subcategory})


def editsubcategory(request,eid):
    categorydata=tbl_category.objects.all()
    editsubcategory=tbl_subcategory.objects.get(id=eid)
    if request.method=="POST":
        category=tbl_category.objects.get(id=request.POST.get("select_category"))
        subcategory=request.POST.get("txt_sub")
        editsubcategory.subcategory_name=subcategory
        editsubcategory.category=category
        editsubcategory.save()
        return redirect("Admin:Subcategory")
    else:
        return render(request,"Admin/Subcategory.html",{'categorydata':categorydata,'editsubcategory':editsubcategory})



def delsubcategory(request,did):
    tbl_subcategory.objects.get(id=did).delete()
    return redirect("Admin:Subcategory")


def sellerview(request):
    seller=tbl_seller.objects.all()
    acceptedlist=tbl_seller.objects.filter(seller_status=1)
    rejectedlist=tbl_seller.objects.filter(seller_status=2)
    return render(request,"Admin/SellerList.html",{'seller':seller,'acceptedlist':acceptedlist,'rejectedlist':rejectedlist})


def userview(request):
     if 'aid' not in request.session:
      return redirect("Guest:Login")
     else:
        users=tbl_user.objects.filter(user_status=0)
        greeting=tbl_AdminRegistration.objects.get(id=request.session['aid'])
        acceptedusers=tbl_user.objects.filter(user_status=1)
        rejectedusers=tbl_user.objects.filter(user_status=2)
        return render(request,"Admin/UserList.html",{'users':users,'acceptedusers':acceptedusers,'rejectedusers':rejectedusers,'greeting':greeting})


        
def acceptseller(request,aid):
    data=tbl_seller.objects.get(id=aid)
    data.seller_status=1
    data.save()
    return render(request,'Admin/SellerList.html',{'msg':"accepted"})

def rejectseller(request,rid):
    data=tbl_seller.objects.get(id=rid)
    data.seller_status=2
    data.save()
    return render(request,'Admin/SellerList.html',{'msg':"rejected"})        


def acceptuser(request,aid):
    data=tbl_user.objects.get(id=aid)
    data.user_status=1
    data.save()
    email=data.user_email
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
    
    return render(request,'Admin/UserList.html',{'msg':"accepted"})

def rejectuser(request,rid):
    data=tbl_user.objects.get(id=rid)
    data.user_status=2
    data.save()
    email=data.user_email
    subject = "GarageLive Account Verification Status"
    message = (
        "Dear User,\n\n"
        "Thank you for registering with GarageLive.\n\n"
        "After reviewing your details, we regret to inform you that your account "
        "could not be approved at this time due to one or more of the following reasons:\n\n"
        "1. Identity verification was not sufficient.\n"
        "2. Required documents were missing or unclear.\n\n"
        "You may reapply by submitting valid proof of identity. "
        "Once submitted, your account will be reviewed and approved within 2–3 working days.\n\n"
        "If you believe this was a mistake, please contact our support team.\n\n"
        "Regards,\n"
        "GarageLive Team"
    )
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    return render(request,'Admin/UserList.html',{'msg':"rejected"})



    
        
def adminhome(request):
     if 'aid' not in request.session:
      return redirect("Guest:Login")
     else:
        admindata=tbl_AdminRegistration.objects.get(id=request.session['aid'])
        return render(request,"Admin/AdminHome.html",{'Data':admindata})



def complaint(request):
     if 'aid' not in request.session:
      return redirect("Guest:Login")
     else:
        complaintdata=tbl_complaint.objects.filter(complaint_status=0)
        replied=tbl_complaint.objects.filter(complaint_status=1)

        return render(request,"Admin/viewcomplaint.html",{'Data':complaintdata,'replied':replied})


def reply(request,cid):

    compdata=tbl_complaint.objects.get(id=cid)
    if request.method=="POST":
        reply=request.POST.get("txt_reply")
        compdata.complaint_reply=reply
        compdata.complaint_status=1
        compdata.save()
        return render(request,"Admin/viewcomplaint.html",{'msg':"Reply Added"})
    else:
        return render(request,"Admin/Reply.html")



def centerlist(request):
     if 'aid' not in request.session:
      return redirect("Guest:Login")
     else:

        centers=tbl_servicecenter.objects.filter(servicecenter_status=0)
        accepted=tbl_servicecenter.objects.filter(servicecenter_status=1)
        rejected=tbl_servicecenter.objects.filter(servicecenter_status=2)
        greeting=tbl_AdminRegistration.objects.get(id=request.session['aid'])

        return render(request,"Admin/Servicecenterverification.html",{'data':centers,'accepted':accepted,'rejected':rejected,'greeting':greeting})


def acceptcenter(request,aid):
    data=tbl_servicecenter.objects.get(id=aid)
    data.servicecenter_status=1
    data.save()
    email=data.servicecenter_email
    subject = "Your GarageLive Service Center Has Been Approved 🚗"
    message = (
        "Dear Service Partner,\n\n"
        "Welcome to GarageLive!\n\n"
        "We are pleased to inform you that your service center registration "
        "has been successfully verified and approved.\n\n"
        "You can now log in to your GarageLive service center dashboard and start:\n\n"
        "• Managing service bookings\n"
        "• Adding and updating services\n"
        "• Tracking customer requests\n"
        "• Managing labour and spare part charges\n\n"
        "Please ensure that your service details and pricing are kept up to date "
        "to provide the best experience for customers.\n\n"
        "If you require any assistance, feel free to reach out to our support team.\n\n"
        "We look forward to working with you.\n\n"
        "Regards,\n"
        "GarageLive Team"
    )
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    
    return render(request,"Admin/Servicecenterverification.html",{'msg':"Service center Accepted"})

def rejectcenter(request,rid):
    data=tbl_servicecenter.objects.get(id=rid)
    data.servicecenter_status=2
    data.save()
    email=data.servicecenter_email
    subject = "GarageLive Service Center Verification Update"
    message = (
        "Dear Service Partner,\n\n"
        "Thank you for registering your service center with GarageLive.\n\n"
        "After reviewing your submitted details, we regret to inform you that "
        "your service center could not be approved at this time due to one or more "
        "of the following reasons:\n\n"
        "1. Business or identity verification was insufficient.\n"
        "2. Required documents were missing or unclear.\n\n"
        "You may reapply by submitting valid business and identity proof. "
        "Once resubmitted, verification will be completed within 2–3 working days.\n\n"
        "If you believe this decision was made in error, please contact our support team.\n\n"
        "Regards,\n"
        "GarageLive Team"
    )
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    return render(request,"Admin/Servicecenterverification.html",{'msg':"Service center Rejected"})


def servicetype(request):
     if 'aid' not in request.session:
      return redirect("Guest:Login")
     else:

        servicetype=tbl_servicetype.objects.all()
        greeting=tbl_AdminRegistration.objects.get(id=request.session['aid'])
        if request.method=="POST":
            service_type=request.POST.get("txt_servicetype")
            tbl_servicetype.objects.create(servicetype_name=service_type)
            return render(request,"Admin/ServiceType.html",{'msg':"Service Type Added"})
        else:
            return render(request,"Admin/ServiceType.html",{'data':servicetype,'greeting':greeting})



def delservicetype(request,did):
    tbl_servicetype.objects.get(id=did).delete()
    return render(request,"Admin/ServiceType.html",{'msg':"Service Type Deleted"})

def editservicetype(request,eid):
    editservice=tbl_servicetype.objects.get(id=eid)
    if request.method=="POST":
        service_type=request.POST.get("txt_servicetype")
        editservice.servicetype_name=service_type
        editservice.save()
        return redirect("Admin:servicetype")
    else:
        return render(request,"Admin/ServiceType.html",{'editservice':editservice})
    



def brand(request):
     if 'aid' not in request.session:
      return redirect("Guest:Login")
     else:
        branddata=tbl_brand.objects.all()
        greeting=tbl_AdminRegistration.objects.get(id=request.session['aid'])
        if request.method=="POST":
            name=request.POST.get("txt_brand")
            tbl_brand.objects.create(brand_name=name)
            return redirect("Admin:brand")

        else:
            return render(request,"Admin/Brand.html",{'data':branddata,'greeting':greeting})

def editbrand(request,eid):
    editdata=tbl_brand.objects.get(id=eid)

    if request.method=="POST":
        brand=request.POST.get("txt_brand")
        editdata.brand_name=brand
        editdata.save()
        return redirect("Admin:brand")
    else:
        return render(request,"Admin/Brand.html",{'editdata':editdata})



def delbrand(request,did):
    tbl_brand.objects.get(id=did).delete()
    return redirect("Admin:brand")



def brand_model(request):
     if 'aid' not in request.session:
      return redirect("Guest:Login")
     else:
        branddata=tbl_brand.objects.all()
    
        greeting=tbl_AdminRegistration.objects.get(id=request.session['aid'])
        selected_brand=request.GET.get("brand")
        if selected_brand:
            modeldata=tbl_model.objects.filter(brand=selected_brand)
        else:
            modeldata=tbl_model.objects.all()


        if request.method=="POST":
            brand=tbl_brand.objects.get(id=request.POST.get("sel_brand"))
            modelname=request.POST.get("txt_model")
            tbl_model.objects.create(model_name=modelname,brand=brand)
            return render(request,"Admin/Model.html",{'msg':"Model Added"})

        else:
            return render(request,"Admin/Model.html",{'branddata':branddata,'modeldata':modeldata,'greeting':greeting,'selected_brand': selected_brand})



def delmodel(request,did):
    tbl_model.objects.get(id=did).delete()
    return redirect("Admin:model")


def editmodel(request,eid):
    branddata=tbl_brand.objects.all()
    editmodel=tbl_model.objects.get(id=eid)
    if request.method=="POST":
        brand=tbl_brand.objects.get(id=request.POST.get("sel_brand"))
        model=request.POST.get("txt_model")
        editmodel.brand=brand
        editmodel.model_name=model
        editmodel.save()
        return redirect("Admin:model")
    else:
        return render(request,"Admin/Model.html",{'editmodel':editmodel,'branddata':branddata})



def logout(request):
    del request.session['aid']
    return redirect("Guest:Login")







def breakdown_servicetype(request):
    if 'aid' not in request.session:
        return redirect("Guest:Login")

    servicetypes = tbl_breakdown_servicetype.objects.all()
    greeting = tbl_AdminRegistration.objects.get(id=request.session['aid'])

    if request.method == "POST":
        service_type = request.POST.get("txt_servicetype")
        tbl_breakdown_servicetype.objects.create(servicetype_name=service_type)
        return render(request,"Admin/BreakdownServiceType.html",{'msg': "Breakdown Service Type Added"})

    return render(request,"Admin/BreakdownServiceType.html",
        {
            'data': servicetypes,
            'greeting': greeting
        }
    )


def edit_breakdown_servicetype(request, eid):
    if 'aid' not in request.session:
        return redirect("Guest:Login")

    editservice = tbl_breakdown_servicetype.objects.get(id=eid)

    if request.method == "POST":
        service_type = request.POST.get("txt_servicetype")
        editservice.servicetype_name = service_type
        editservice.save()
        return redirect("Admin:breakdown_servicetype")

    return render(request,"Admin/BreakdownServiceType.html",{'editservice': editservice})


def del_breakdown_servicetype(request, did):
    if 'aid' not in request.session:
        return redirect("Guest:Login")

    tbl_breakdown_servicetype.objects.get(id=did).delete()
    return render(request,"Admin/BreakdownServiceType.html",{'msg': "Breakdown Service Type Deleted"})
