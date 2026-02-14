from django.shortcuts import render,redirect
from Guest.models import *
from ServiceCenter.models import *
from Admin.models import *
from User.models import *
from decimal import Decimal
from datetime import date, timedelta
from django.db.models import Count
from django.db.models import Q
from django.http import JsonResponse
import calendar
from django.db.models import Sum
from collections import defaultdict






# Create your views here.

def homepage(request):
     if 'cid' not in request.session:
      return redirect("Guest:Login")
     else:
        centerdata=tbl_servicecenter.objects.get(id=request.session['cid'])
        today = date.today()
       
        
        active_jobs = tbl_booking.objects.filter(servicecenter=centerdata).filter(Q(booking_status=1) | Q(booking_status__gte=3, booking_status__lt=12)).count()
        active_breakdown_jobs=tbl_breakdownassist.objects.filter(servicecenter=centerdata, breakdown_status=1).count()
        
        pending_service_approvals=tbl_booking.objects.filter(servicecenter=centerdata, booking_status=0).count()
        pending_breakdown_approvals=tbl_breakdownassist.objects.filter(servicecenter=centerdata, breakdown_status=0).count()
        customer_feedback_count = tbl_feedback.objects.filter(servicecenter=centerdata,feedback_date__month=today.month,feedback_date__year=today.year).count()
        technicians = tbl_technician.objects.filter(servicecenter=centerdata)
        busy_tech_ids=get_busy_technician_ids(centerdata)

        technician_status_list = []
        for tech in technicians:
            service_completed=tbl_booking.objects.filter(servicecenter=centerdata,technician=tech,booking_status=12).count()
            breakdown_completed=tbl_breakdownassist.objects.filter(servicecenter=centerdata,technician=tech,breakdown_status=3).count()
            total_completed= service_completed+ breakdown_completed
            is_busy = tech.id in busy_tech_ids
            technician_status_list.append({"technician": tech,"is_busy": is_busy,"total_completed": total_completed})
        technician_status_list.sort(key=lambda x: x['total_completed'],reverse=True)





        return render(request,"ServiceCenter/HomePage.html",{'data':centerdata,
        'active_jobs':active_jobs,'pending_service_approvals':pending_service_approvals,'pending_breakdown_approvals':pending_breakdown_approvals,'customer_feedback_count':customer_feedback_count,
        'active_breakdown_jobs':active_breakdown_jobs,"technician_status_list": technician_status_list})



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
            return render(request,"ServiceCenter/ChangePassword.html",{'Data':changepass})



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
            return render(request,"ServiceCenter/Technician.html",{'data':techniciandata,'Data':servicecenter})


def deltechnician(request,did):
    tbl_technician.objects.get(id=did).delete()
    return render(request,"ServiceCenter/Technician.html",{'msg':"Technician Removed"})



def myservices(request):
     if 'cid' not in request.session:
      return redirect("Guest:Login")
     else:
        servicetype=tbl_servicetype.objects.all()
        servicecenter=tbl_servicecenter.objects.get(id=request.session['cid'])
        myservices=tbl_servicecenterservices.objects.filter(servicecenter=request.session['cid'])
        if request.method=="POST":
            service_type=tbl_servicetype.objects.get(id=request.POST.get("sel_servicetype"))
            servicecenter=tbl_servicecenter.objects.get(id=request.session['cid'])
            base_amount=request.POST.get("base_amount")
            tbl_servicecenterservices.objects.create(servicetype=service_type,servicecenter=servicecenter,base_amount=base_amount)
            return render(request,"ServiceCenter/MyServices.html",{'msg':"Service added"})
        else:
            return render(request,"ServiceCenter/MyServices.html",{'data':servicetype,'myservices':myservices,'Data':servicecenter})



def editmy_services(request, sid):
    editservice = tbl_servicecenterservices.objects.get(id=sid)
    servicetype = tbl_servicetype.objects.all()   
    myservices = tbl_servicecenterservices.objects.filter(servicecenter=request.session['cid']) 
    servicecenter=tbl_servicecenter.objects.get(id=request.session['cid'])
    if request.method == "POST":
        base_amount = request.POST.get("base_amount")
        editservice.base_amount = base_amount
        editservice.save()
        return redirect("ServiceCenter:myservices")
    else:
        return render(request, "ServiceCenter/MyServices.html", {
            'editservice': editservice,
            'data': servicetype,        
            'myservices': myservices,'Data':servicecenter    
        })

        

        


def delmyservices(request,did):
    tbl_servicecenterservices.objects.get(id=did).delete()
    return redirect("ServiceCenter:myservices")


def service_requests(request):
    if 'cid' not in request.session:
      return redirect("Guest:Login")
    else:
        servicecenter=tbl_servicecenter.objects.get(id=request.session['cid'])
        bookingdata=tbl_booking.objects.filter(servicecenter_id=request.session['cid']).order_by('-id')
        for booking in bookingdata:
            booking.services=tbl_booking_services.objects.filter(booking=booking)
        return render(request,"ServiceCenter/ServiceRequest.html",{'data':bookingdata,'Data': servicecenter})



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
    servicecenter=tbl_servicecenter.objects.get(id=request.session['cid'])
    busy_ids = get_busy_technician_ids(servicecenter)
    return render(request,"ServiceCenter/AssignTechnician.html",{'data':technician_data,'bid':bid,'busy_ids': list(busy_ids),'mode': 'service','Data':servicecenter})

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
        admin_amount=total_amount*Decimal('0.05')
        tbl_commision.objects.create(servicecenter=booking.servicecenter,booking_type=1,booking_id=booking.id,admin_commision=admin_amount)

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
    servicecenter=tbl_servicecenter.objects.get(id=request.session['cid'])
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
        {"services": services,'Data': servicecenter}
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
    return render(request,"ServiceCenter/Breakdown.html",{'msg':"Request Rejected"})


def breakdown_technician(request,btid):
    technician_data=tbl_technician.objects.filter(servicecenter=request.session['cid'])
    servicecenter=tbl_servicecenter.objects.get(id=request.session['cid'])
    busy_ids = get_busy_technician_ids(servicecenter)

    return render(request,"ServiceCenter/AssignTechnician.html",{'data':technician_data,'btid':btid,'busy_ids': list(busy_ids),'mode': 'breakdown','Data':servicecenter})


def get_busy_technician_ids(servicecenter):

    # Busy from Service Bookings
    busy_service_ids = tbl_booking.objects.filter(
        servicecenter=servicecenter,
        booking_status__in=[1,2,3],  # active statuses
        technician__isnull=False
    ).values_list('technician_id', flat=True)

    # Busy from Breakdown Jobs
    busy_breakdown_ids = tbl_breakdownassist.objects.filter(
        servicecenter=servicecenter,
        breakdown_status=1,
        technician__isnull=False
    ).values_list('technician_id', flat=True)

    return set(busy_service_ids) | set(busy_breakdown_ids)




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
    servicecenter=tbl_servicecenter.objects.get(id=request.session['cid'])

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
            'myservices': myservices,'Data': servicecenter
        }
    )


def edit_breakdown_service(request, sid):
    editservice = tbl_servicecenter_breakdown_services.objects.get(id=sid)
    servicecenter=tbl_servicecenter.objects.get(id=request.session['cid'])

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
            'myservices': myservices,
            'Data': servicecenter
        }
    )


def delete_breakdown_service(request, did):
    tbl_servicecenter_breakdown_services.objects.get(id=did).delete()
    return redirect("ServiceCenter:my_breakdown_services")




def view_feedback(request):
    servicecenter=tbl_servicecenter.objects.get(id=request.session['cid'])
    feedbacks=tbl_feedback.objects.filter(servicecenter=servicecenter)
    return render(request,"ServiceCenter/Feedback.html",{'feedbacks': feedbacks,'Data': servicecenter}) 



def chart_homepage(request):
    servicecenter_id = request.session.get('cid')

    if not servicecenter_id:
        return JsonResponse({"days": [], "service": [], "breakdown": []})

    today = date.today()
    year = today.year
    month = today.month

    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])

    labels = []
    service_counts = []
    breakdown_counts = []

    # Pre-fetch all data for the month (reduces DB queries)
    service_bookings = tbl_booking.objects.filter(
        servicecenter_id=servicecenter_id,
        booking_date__range=(first_day, last_day)
    ).values_list('booking_date', flat=True)

    breakdown_bookings = tbl_breakdownassist.objects.filter(
        servicecenter_id=servicecenter_id,
        breakdown_date__range=(first_day, last_day)
    ).values_list('breakdown_date', flat=True)

    # Convert to sets for faster lookups
    service_dates = list(service_bookings)
    breakdown_dates = list(breakdown_bookings)

    current_start = first_day
    week_number = 1

    while current_start <= last_day:
        current_end = min(current_start + timedelta(days=6), last_day)
        
        labels.append(f"Week {week_number}")

        # Count bookings in the current week range
        service_count = sum(1 for d in service_dates if current_start <= d <= current_end)
        breakdown_count = sum(1 for d in breakdown_dates if current_start <= d <= current_end)

        service_counts.append(service_count)
        breakdown_counts.append(breakdown_count)

        current_start = current_end + timedelta(days=1)
        week_number += 1

    return JsonResponse({
        "days": labels,
        "service": service_counts,
        "breakdown": breakdown_counts
    })



def weekly_income_chart(request):

    servicecenter_id = request.session.get('cid')

    if not servicecenter_id:
        return JsonResponse({"weeks": [], "service": [], "breakdown": []})

    today = date.today()
    year = today.year
    month = today.month

    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])

    labels = []
    service_income = []
    breakdown_income = []

    current_start = first_day
    week_number = 1

    while current_start <= last_day:

        current_end = current_start + timedelta(days=6)
        if current_end > last_day:
            current_end = last_day

        labels.append(f"Week {week_number}")

        # Service Income
        service_total = tbl_booking_services.objects.filter(
            booking__servicecenter_id=servicecenter_id,
            booking__booking_date__range=(current_start, current_end)
        ).aggregate(total=Sum('final_amount'))['total'] or 0

        # Breakdown Income
        breakdown_total = tbl_breakdown_booking_services.objects.filter(
            booking__servicecenter_id=servicecenter_id,
            booking__breakdown_date__range=(current_start, current_end)
        ).aggregate(total=Sum('final_amount'))['total'] or 0

        service_income.append(float(service_total))
        breakdown_income.append(float(breakdown_total))

        current_start = current_end + timedelta(days=1)
        week_number += 1
        total_service_income = sum(service_income)
        total_breakdown_income = sum(breakdown_income)


    return JsonResponse({
        "weeks": labels,
        "service": service_income,
        "breakdown": breakdown_income,
        "total_service": float(total_service_income),
        "total_breakdown": float(total_breakdown_income)
    })






