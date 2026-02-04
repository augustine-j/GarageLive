from django.shortcuts import render,redirect
from Guest.models import *
from ServiceCenter.models import *
from Admin.models import *
from User.models import *
from decimal import Decimal

# Create your views here.

def homepage(request):
     if 'cid' not in request.session:
      return redirect("Guest:Login")
     else:
        centerdata=tbl_servicecenter.objects.get(id=request.session['cid'])
        return render(request,"ServiceCenter/HomePage.html",{'data':centerdata})



def profile(request):
     if 'cid' not in request.session:
      return redirect("Guest:Login")
     else:
        centerdata=tbl_servicecenter.objects.get(id=request.session['cid'])
        return render(request,"ServiceCenter/Profile.html",{'Data':centerdata})


def editprofile(request):
     if 'cid' not in request.session:
      return redirect("Guest:Login")
     else:
        editprofile=tbl_servicecenter.objects.get(id=request.session['cid'])
        if request.method=="POST":
            name=request.POST.get("txt_name")
            email=request.POST.get("txt_email")
            contact=request.POST.get("txt_contact")
            address=request.POST.get("txt_address")
            logo=request.FILES.get("file_logo")
            editprofile.servicecenter_name=name
            editprofile.servicecenter_email=email
            editprofile.servicecenter_contact=contact
            editprofile.servicecenter_address=address
            editprofile.servicecenter_logo=logo
            editprofile.save()
            return render(request,"ServiceCenter/Profile.html",{'msg':"Record Updated"})
        else:
            return render(request,"ServiceCenter/EditProfile.html",{'Data':editprofile})



def changepassword(request):
     if 'cid' not in request.session:
      return redirect("Guest:Login")
     else:

        changepass=tbl_servicecenter.objects.get(id=request.session['cid'])
        dbpass=changepass.servicecenter_password
        if request.method=="POST":
            old=request.POST.get("txt_password")
            new=request.POST.get("new_password")
            confirm=request.POST.get("confirm_password")
            if old==dbpass:
                if new==confirm:
                    changepass.servicecenter_password=new
                    changepass.save()
                    return render(request,"ServiceCenter/Profile.html",{'msg':"Password Updated"})
                else:
                    return render(request,"ServiceCenter/ChangePassword.html",{'msg':"Invalid Password"})
            else:
                return render(request,"ServiceCenter/ChangePassword.html",{'msg':"Passwords dont match"})
            
        else:
            return render(request,"ServiceCenter/ChangePassword.html")



def technician(request):
     if 'cid' not in request.session:
      return redirect("Guest:Login")
     else:
        techniciandata=tbl_technician.objects.filter(servicecenter=request.session['cid'])
        servicecenter=tbl_servicecenter.objects.get(id=request.session['cid'])
        if request.method=="POST":
            name=request.POST.get("txt_name")
            email=request.POST.get("txt_mail")
            contact=request.POST.get("txt_contact")
            photo=request.FILES.get("photo")
            password=request.POST.get("txt_password")

            techniciancount=tbl_technician.objects.filter(technician_email=email).count()
            if techniciancount>0:
                return render(request,"ServiceCenter/Technician.html",{'msg':"email already exists"})
            else:

                tbl_technician.objects.create(technician_name=name,technician_email=email,technician_contact=contact,
                technician_photo=photo,technician_password=password,servicecenter=servicecenter)
                return render(request,"ServiceCenter/Technician.html",{'msg':"Technician Added"})
        else:
            return render(request,"ServiceCenter/Technician.html",{'data':techniciandata})


def deltechnician(request,did):
    tbl_technician.objects.get(id=did).delete()
    return render(request,"ServiceCenter/Technician.html",{'msg':"Technician Removed"})



def myservices(request):
     if 'cid' not in request.session:
      return redirect("Guest:Login")
     else:
        servicetype=tbl_servicetype.objects.all()
        myservices=tbl_servicecenterservices.objects.filter(servicecenter=request.session['cid'])
        if request.method=="POST":
            service_type=tbl_servicetype.objects.get(id=request.POST.get("sel_servicetype"))
            servicecenter=tbl_servicecenter.objects.get(id=request.session['cid'])
            base_amount=request.POST.get("base_amount")
            tbl_servicecenterservices.objects.create(servicetype=service_type,servicecenter=servicecenter,base_amount=base_amount)
            return render(request,"ServiceCenter/MyServices.html",{'msg':"Service added"})
        else:
            return render(request,"ServiceCenter/MyServices.html",{'data':servicetype,'myservices':myservices})



def editmy_services(request, sid):
    editservice = tbl_servicecenterservices.objects.get(id=sid)
    servicetype = tbl_servicetype.objects.all()   
    myservices = tbl_servicecenterservices.objects.filter(servicecenter=request.session['cid']) 
    if request.method == "POST":
        base_amount = request.POST.get("base_amount")
        editservice.base_amount = base_amount
        editservice.save()
        return redirect("ServiceCenter:myservices")
    else:
        return render(request, "ServiceCenter/MyServices.html", {
            'editservice': editservice,
            'data': servicetype,        
            'myservices': myservices    
        })

        

        


def delmyservices(request,did):
    tbl_servicecenterservices.objects.get(id=did).delete()
    return redirect("ServiceCenter:myservices")


def service_requests(request):
    bookingdata=tbl_booking.objects.filter(servicecenter_id=request.session['cid'])
    for booking in bookingdata:
        booking.services=tbl_booking_services.objects.filter(booking=booking)
    return render(request,"ServiceCenter/ServiceRequest.html",{'data':bookingdata})



def acceptrequest(request,aid):
    data=tbl_booking.objects.get(id=aid)
    data.booking_status=1
    data.save()
    return render(request,"ServiceCenter/ServiceRequest.html",{'msg':"Request Accepted"})


def rejectrequest(request,rid):
    data=tbl_booking.objects.get(id=rid)
    data.booking_status=2
    data.save()
    return render(request,"ServiceCenter/ServiceRequest.html",{'msg':"Request Rejected"})


def assign_technician(request,bid):
    technician_data=tbl_technician.objects.filter(servicecenter=request.session['cid'])
    busy_ids = tbl_booking.objects.filter(booking_status__in=[1, 3, 4, 5, 6, 7, 8]).values_list('technician_id', flat=True)
    return render(request,"ServiceCenter/AssignTechnician.html",{'data':technician_data,'bid':bid,'busy_ids': list(busy_ids),'mode': 'service'})

def assignjob(request,tid,bid):
    technician=tbl_technician.objects.get(id=tid)
    booking=tbl_booking.objects.get(id=bid)
    booking.technician_id=technician
    booking.save()

    return render(request,"ServiceCenter/ServiceRequest.html",{'msg':"Technician Assigned"})





def generate_bill(request, bid):

    booking = tbl_booking.objects.get(id=bid)

    services = tbl_booking_services.objects.filter(booking=booking)

    total_amount = Decimal('0.00')
    for s in services:
        total_amount += s.final_amount or Decimal('0.00')

    if request.method == "POST":
        booking.booking_status = 11  
        booking.save()

        return redirect("ServiceCenter:service_request")

    return render(
        request,
        "ServiceCenter/Bill.html",
        {
            "booking": booking,
            "services": services,
            "total_amount": total_amount
        }
    )



def logout(request):
    del request.session['cid']
    return redirect("Guest:Login")



def breakdown_requests(request):
    services = tbl_breakdown_booking_services.objects.filter(
        booking__servicecenter_id=request.session['cid']
    ).select_related(
        "booking",
        "booking__user",
        "booking__vehicle",
        "booking__vehicle__model__brand",
        "booking__technician",
        "servicecenter_breakdown_service__servicetype"
    ).order_by('-id')

    return render(
        request,
        "ServiceCenter/Breakdown.html",
        {"services": services}
    )



def acceptbreakdown(request,aid):
    data=tbl_breakdownassist.objects.get(id=aid)
    data.breakdown_status=1
    data.save()
    return render(request,"ServiceCenter/Breakdown.html",{'msg':"Request Accepted"})

def rejectbreakdown(request,rid):
    data=tbl_breakdownassist.objects.get(id=rid)
    data.breakdown_status=2
    data.save()
    return render(request,"ServiceCenter/Breakdown.html",{'msg':"Request Accepted"})


def breakdown_technician(request,btid):
    technician_data=tbl_technician.objects.filter(servicecenter=request.session['cid'])
    busy_ids = tbl_breakdown_booking_services.objects.filter(
    booking__technician__isnull=False,
    billing_status=False).values_list('booking__technician_id',flat=True).distinct()

    return render(request,"ServiceCenter/AssignTechnician.html",{'data':technician_data,'btid':btid,'busy_ids': list(busy_ids),'mode': 'breakdown'})

def assign_breakdown(request,tid,btid):
    technician=tbl_technician.objects.get(id=tid)
    booking=tbl_breakdownassist.objects.get(id=btid)
    booking.technician_id=technician
    booking.save()

    return render(request,"ServiceCenter/Breakdown.html",{'msg':"Technician Assigned"})





def my_breakdown_services(request):
    if 'cid' not in request.session:
        return redirect("Guest:Login")

    servicetypes = tbl_breakdown_servicetype.objects.all()
    myservices = tbl_servicecenter_breakdown_services.objects.filter(servicecenter=request.session['cid'])

    if request.method == "POST":
        servicetype = tbl_breakdown_servicetype.objects.get(id=request.POST.get("sel_servicetype"))
        servicecenter = tbl_servicecenter.objects.get(id=request.session['cid'])
        base_amount = request.POST.get("base_amount")

        tbl_servicecenter_breakdown_services.objects.create(
            servicetype=servicetype,
            servicecenter=servicecenter,
            base_amount=base_amount
        )

        return render(request,"ServiceCenter/MyBreakdownServices.html",{'msg': "Breakdown service added"})

    return render(request,"ServiceCenter/MyBreakdownServices.html",
        {
            'data': servicetypes,
            'myservices': myservices
        }
    )


def edit_breakdown_service(request, sid):
    editservice = tbl_servicecenter_breakdown_services.objects.get(id=sid)

    if request.method == "POST":
        editservice.base_amount = request.POST.get("base_amount")
        editservice.save()
        return redirect("ServiceCenter:my_breakdown_services")

    servicetypes = tbl_breakdown_servicetype.objects.all()
    myservices = tbl_servicecenter_breakdown_services.objects.filter(servicecenter=request.session['cid'])

    return render( request, "ServiceCenter/MyBreakdownServices.html",
        {
            'editservice': editservice,
            'data': servicetypes,
            'myservices': myservices
        }
    )


def delete_breakdown_service(request, did):
    tbl_servicecenter_breakdown_services.objects.get(id=did).delete()
    return redirect("ServiceCenter:my_breakdown_services")


