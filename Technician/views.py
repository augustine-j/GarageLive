from django.shortcuts import render,redirect
from ServiceCenter.models import *
from User.models import *
from Technician.models import *
from decimal import Decimal



# Create your views here.


def homepage(request):
     if 'tid' not in request.session:
      return redirect("Guest:Login")
     else:
        greeting=tbl_technician.objects.get(id=request.session['tid'])
        techniciandata=tbl_technician.objects.get(id=request.session['tid'])
        assigned_service_jobs=tbl_booking.objects.filter(technician=techniciandata,booking_status__gte=1,booking_status__lte=10).prefetch_related('tbl_booking_services_set')
        
        assigned_breakdown_jobs=tbl_breakdownassist.objects.filter(technician=techniciandata,breakdown_status=1)
        completed_service_count=tbl_booking.objects.filter(technician=techniciandata,booking_status=12).count()
        completed_breakdown_count=tbl_breakdownassist.objects.filter(technician=techniciandata,breakdown_status=3).count()
        



        return render(request,"Technician/HomePage.html",{'data':techniciandata,'greeting':greeting,
        "assigned_service_jobs": assigned_service_jobs,
        "assigned_breakdown_jobs": assigned_breakdown_jobs,
        "assigned_total": assigned_service_jobs.count() + assigned_breakdown_jobs.count(),
        "total_completed": completed_service_count + completed_breakdown_count})

def profile(request):
     if 'tid' not in request.session:
      return redirect("Guest:Login")
     else:
        technician=tbl_technician.objects.get(id=request.session['tid'])
        greeting=tbl_technician.objects.get(id=request.session['tid'])
        return render(request,"Technician/Profile.html",{'data':technician,'greeting':greeting})


def editprofile(request):
     if 'tid' not in request.session:
      return redirect("Guest:Login")
     else:
        editprofile=tbl_technician.objects.get(id=request.session['tid'])
        greeting=tbl_technician.objects.get(id=request.session['tid'])
        if request.method=="POST":
            name=request.POST.get("txt_name")
            email=request.POST.get("txt_email")
            contact=request.POST.get("txt_contact")
            photo=request.FILES.get("file_photo")
            editprofile.technician_name=name
            editprofile.technician_email=email
            editprofile.technician_contact=contact
            editprofile.technician_photo=photo
            editprofile.save()
            return render(request,"Technician/Profile.html",{'msg':"Record Updated"})
        else:
            return render(request,"Technician/EditProfile.html",{'data':editprofile},{'greeting':greeting})


def changepassword(request):
     if 'tid' not in request.session:
      return redirect("Guest:Login")
     else:
        changepass=tbl_technician.objects.get(id=request.session['tid'])
        greeting=tbl_technician.objects.get(id=request.session['tid'])
        dbpass=changepass.technician_password
        if request.method=="POST":
            old=request.POST.get("txt_password")
            new=request.POST.get("new_password")
            confirm=request.POST.get("confirm_password")
            if old==dbpass:
                if new==confirm:
                    changepass.technician_password=new
                    changepass.save()
                    return render(request,"Technician/Profile.html",{'msg':"Password updated"})
                else:
                    return render(request,"Technician/ChangePassword.html",{'msg':"Invalid Password"})
            else:
                return render(request,"Technician/ChangePassword.html",{'msg':"Passwords doesn't match"})
        else:
            return render(request,"Technician/ChangePassword.html",{'greeting':greeting})




def assigned_jobs(request):
    if 'tid' not in request.session:
      return redirect("Guest:Login")
    else:
        greeting=tbl_technician.objects.get(id=request.session['tid'])
        jobdata=tbl_booking.objects.filter(technician=request.session['tid']).order_by('-id') 
        for booking in jobdata:
            booking.services = tbl_booking_services.objects.filter(booking=booking)

        return render(request,"Technician/Jobs.html",{'data':jobdata,'greeting':greeting})


def startwork(request,sid):
    data=tbl_booking.objects.get(id=sid)
    data.booking_status=3
    data.save()
    return redirect("Technician:assigned_jobs")


def start_diagnosis(request,did):
    data=tbl_booking.objects.get(id=did)
    data.booking_status=4
    data.save()
    return redirect("Technician:assigned_jobs")

def diagnosis_completed(request,cdid):
    data=tbl_booking.objects.get(id=cdid)
    data.booking_status=5
    data.save()
    return redirect("Technician:assigned_jobs")

def repair_progress(request,rid):
    data=tbl_booking.objects.get(id=rid)
    data.booking_status=6
    data.save()
    return redirect("Technician:assigned_jobs")

def parts_replaced(request,pid):
    data=tbl_booking.objects.get(id=pid)
    data.booking_status=7
    data.save()
    return redirect("Technician:assigned_jobs")

def testing_QA(request,tid):
    data=tbl_booking.objects.get(id=tid)
    data.booking_status=8
    data.save()
    return redirect("Technician:assigned_jobs")

def service_completed(request,sid):
    data=tbl_booking.objects.get(id=sid)
    data.booking_status=9
    data.save()
    return redirect("Technician:assigned_jobs")

def out_delivery(request,did):
    data=tbl_booking.objects.get(id=did)
    data.booking_status=10
    data.save()
    return redirect("Technician:assigned_jobs")

# def delivered(request,did):
#     data=tbl_booking.objects.get(id=did)
#     data.booking_status=12
#     data.save()
#     return render(request,"Technician/Jobs.html",{'msg':"Vehicle Delivered"})
    


def workdescription(request,bid):
    greeting=tbl_technician.objects.get(id=request.session['tid'])
    bookingdata=tbl_booking.objects.get(id=bid)    
    notes=tbl_workedescription.objects.filter(booking=bookingdata)
    if request.method=="POST":
        work=request.POST.get("txt_work")
        tbl_workedescription.objects.create(workedesc_content=work,booking=bookingdata)
        return render(request,"Technician/Jobs.html",{'msg':"Note Added"})

    else:
        return render(request,"Technician/WorkDescription.html",{'notes':notes,'greeting':greeting})



def logout(request):
    del request.session['tid']
    return redirect("Guest:Login")



def update_service_cost(request, booking_id):

    booking = tbl_booking.objects.get(id=booking_id)
    greeting=tbl_technician.objects.get(id=request.session['tid'])
    services = tbl_booking_services.objects.filter(booking=booking)
    if booking.booking_status >= 10:
        return redirect("Technician:assigned_jobs")
    
    else:


        if request.method == "POST":
            for service in services:
                labour = request.POST.get(f"labour_{service.id}")
                parts = request.POST.get(f"parts_{service.id}")

                service.labour_charge = Decimal(labour)
                service.parts_charge = Decimal(parts)
                service.final_amount = (
                    service.base_amount +
                    service.labour_charge +
                    service.parts_charge 
                    
                )
                service.save()

            return redirect("Technician:assigned_jobs")

    return render(
        request,
        "Technician/ServiceCost.html",
        {
            "booking": booking,
            "services": services,'greeting':greeting
        }
    )




def breakdown_jobs(request):
    if 'tid' not in request.session:
        return redirect("Guest:Login")
    greeting=tbl_technician.objects.get(id=request.session['tid'])
    data = tbl_breakdown_booking_services.objects.filter(booking__technician_id=request.session['tid']).order_by('-id')
    return render(request, "Technician/BreakdownJobs.html", {'data': data,'greeting':greeting})


def update_breakdown_step(request, sid):
    service = tbl_breakdown_booking_services.objects.get(id=sid)
    service.progress_step += 1
    service.save()
    return redirect("Technician:breakdown_jobs")


def update_breakdown_charge(request, bs_id):
    bs = tbl_breakdown_booking_services.objects.get(id=bs_id)
    breakdown_bs = tbl_breakdownassist.objects.get(id=bs.booking_id)
    greeting=tbl_technician.objects.get(id=request.session['tid'])
    

    if bs.progress_step < 1:
        return redirect("Technician:breakdown_jobs")

    if request.method == "POST":
        extra = Decimal(request.POST.get("extra_charge", 0))

        bs.extra_charge = extra
        bs.final_amount = bs.base_amount + extra
        bs.progress_step += 1
        bs.billing_status = True
        breakdown_bs.breakdown_status = 3
        bs.save()
        breakdown_bs.save()

        total_amount=bs.final_amount
        breakdown_booking=bs.booking
        servicecenter=breakdown_booking.servicecenter

        if not tbl_commision.objects.filter(booking_type=2,booking_id=breakdown_booking.id).exists():
            admin_amount=total_amount * Decimal('0.05')

            tbl_commision.objects.create(
                servicecenter=servicecenter,
                booking_type=2,
                booking_id=breakdown_booking.id,
                admin_commision=admin_amount,
            )
            

        

        return redirect("Technician:breakdown_jobs")

    return render(request, "Technician/UpdateBreakdownCharge.html", {
        "data": bs,'greeting':greeting
    })







