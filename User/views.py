from django.shortcuts import render,redirect

from Admin.models import *
from Guest.models import *
from User.models import *
from ServiceCenter.models import *
from Technician.models import *
from decimal import Decimal
from django.db.models import Sum
from datetime import date
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Avg, Count







def myprofile(request):
   if 'uid' not in request.session:
      return redirect("Guest:Login")
   else:
      userdata=tbl_user.objects.get(id=request.session['uid'])
      greeting=tbl_user.objects.get(id=request.session['uid'])
      return render(request,"User/MyProfile.html",{'Data':userdata,'greeting':greeting})



def editprofile(request):
   if 'uid' not in request.session:
      return redirect("Guest:Login")
   else:
      editprofile=tbl_user.objects.get(id=request.session['uid'])
   

      if request.method=="POST":
         name=request.POST.get("txt_name")
         email=request.POST.get("txt_email")
         contact=request.POST.get("txt_contact")
         address=request.POST.get("txt_address")
         editprofile.user_name=name
         editprofile.user_email=email
         editprofile.contact_number=contact
         editprofile.address=address
         editprofile.save()
         return render(request,"User/MyProfile.html",{'msg':"Data Updated"})
      else:
         return render(request,"User/EditProfile.html",{'editprofile':editprofile})


def changepassword(request):
    if 'uid' not in request.session:
      return redirect("Guest:Login")
    else:
      userdata=tbl_user.objects.get(id=request.session['uid'])
      dbpass=userdata.password
      if request.method=="POST":
         old=request.POST.get("txt_password")
         new=request.POST.get("new_password")
         confirm=request.POST.get("confirm_password")
         if old==dbpass:
            if new==confirm:
               userdata.password=new
               userdata.save()
               return render(request,"User/MyProfile.html",{'msg':"Password Updated"})
            else:
               return render(request,"User/ChangePassword.html",{'msg':"Invalid Password"})
         else:
            return render(request,"User/ChangePassword.html",{'msg':"Invalid Password"})
      
      else:
         return render(request,"User/ChangePassword.html",{'data':userdata})
      


def complaint(request):
    if 'uid' not in request.session:
      return redirect("Guest:Login")
    else:
      userdata=tbl_user.objects.get(id=request.session['uid'])
      complaintdata=tbl_complaint.objects.filter(user=request.session['uid'])
      if request.method=="POST":
         title=request.POST.get("txt_title")
         content=request.POST.get("txt_content")
         tbl_complaint.objects.create(complaint_title=title,complaint_content=content,user=userdata)
         return render(request,"User/HomePage.html",{'msg':"Compliant Registered"})
      else:
         return render(request,"User/Complaint.html",{'Data':complaintdata})


def delcomplaint(request,did):
   tbl_complaint.objects.get(id=did).delete()
   return redirect("User:complaint")


  
      




def homepageview(request):
   if 'uid' not in request.session:
      return redirect("Guest:Login")
   else:

      userdata=tbl_user.objects.get(id=request.session['uid'])
      return render(request,"User/HomePage.html",{'Data':userdata})




def viewservicecenter(request):
    if 'uid' not in request.session:
      return redirect("Guest:Login")
    else:

      districtdata=tbl_district.objects.all()
      greeting=tbl_user.objects.get(id=request.session['uid'])
      placedata=tbl_place.objects.all()
   
      if request.method=="POST":
         servicecenter=tbl_servicecenter.objects.filter(place=request.POST.get("sel_place"),servicecenter_status=1).annotate(avg_rating=Avg('feedbacks__rating'),total_reviews=Count('feedbacks'))
         return render(request,"User/ViewServiceCenter.html",{'servicecenter':servicecenter,})

      else:
         return render(request,"User/ViewServiceCenter.html",{'districtdata':districtdata,'placedata':placedata,'greeting':greeting})


def AjaxLocation(request):
    districtid=request.GET.get('did')
    placedata=tbl_place.objects.filter(district=districtid)
    return render(request,'User/AjaxLocation.html',{'placedata':placedata})



def servicebooking(request,sid):
    if 'uid' not in request.session:
      return redirect("Guest:Login")
    else:

        user=tbl_user.objects.get(id=request.session['uid'])
        greeting=tbl_user.objects.get(id=request.session['uid'])
        servicecenter=tbl_servicecenter.objects.get(id=sid)
        servicetype=tbl_servicecenterservices.objects.filter(servicecenter_id=sid)
        vehicle_data=tbl_vehicle.objects.filter(user_id=request.session['uid'])
        today = date.today().isoformat()
        


        if request.method=="POST":
            todate=request.POST.get("txt_date")
            complaint=request.POST.get("txt_complaint")
            
            vehicle=tbl_vehicle.objects.get(id=request.POST.get("sel_vehicle"))
            service_ids=request.POST.getlist("services")

            booking=tbl_booking.objects.create(booking_todate=todate,booking_complaints=complaint,user=user,
            servicecenter=servicecenter,vehicle=vehicle)

            for service_id in service_ids:
                sc_service=tbl_servicecenterservices.objects.get(id=service_id)
                tbl_booking_services.objects.create(booking=booking,servicecenter_services=sc_service,
                base_amount=sc_service.base_amount)

            return render(request,"User/HomePage.html",{'msg':"Service Booked"})
        return render(request,"User/ServiceBooking.html",{'data':servicetype,'vehicle_data':vehicle_data,'greeting':greeting,'today':today})



def myservice_request(request):
    if 'uid' not in request.session:
      return redirect("Guest:Login")
    else:
      bookingdata=tbl_booking.objects.filter(user=request.session['uid']).order_by('-id')
      
      greeting=tbl_user.objects.get(id=request.session['uid'])
      
      for booking in bookingdata:
         booking.services=tbl_booking_services.objects.filter(booking=booking)

       

      return render(request,"User/MyServiceRequest.html",{'data':bookingdata,'greeting':greeting})






def AjaxVehicle(request):
    brandid=request.GET.get('bid')
    modeldata=tbl_model.objects.filter(brand=brandid)
    return render(request,'User/AjaxVehicle.html',{'modeldata':modeldata})



def vehicle(request):
    if 'uid' not in request.session:
      return redirect("Guest:Login")
    else:
      branddata=tbl_brand.objects.all()
      modeldata=tbl_model.objects.all()
      userdata=tbl_user.objects.get(id=request.session['uid'])

      if request.method=="POST":
         vehicle_number=request.POST.get("txt_number")
         year=request.POST.get("txt_year")
         model=tbl_model.objects.get(id=request.POST.get("sel_model"))
         photo=request.FILES.get("vehicle_image")
         tbl_vehicle.objects.create(vehicle_number=vehicle_number,vehicle_year=year,model=model,vehicle_photo=photo,user=userdata)
         return render(request,"User/Vehicle.html",{'msg':"Vehicle Added"})

      return render(request,"User/Vehicle.html",{'branddata':branddata,'modeldata':modeldata,'greeting':userdata})



def worknote(request,bid):
   bookingdata=tbl_booking.objects.get(id=bid)
   notes=tbl_workedescription.objects.filter(booking=bookingdata)
   return render(request,"User/ServiceNotes.html",{'notes':notes})




def payment(request, bid):

    booking = tbl_booking.objects.get(id=bid)

    services = tbl_booking_services.objects.filter(booking=booking)

    total_amount = Decimal('0.00')
    for s in services:
        total_amount += s.final_amount or Decimal('0.00')
    if not booking.booking_status == 11:
        return redirect("User:myservicerequest")

    if request.method == "POST":
        booking.booking_status = 12  
        booking.save()

        return redirect("User:myservicerequest")

    return render(
        request,
        "User/Payment.html",
        {
            "booking": booking,
            "services": services,
            "total_amount": total_amount
        }
    )


   

      



def invoice(request, bid):
    booking = tbl_booking.objects.get(id=bid)

    services = tbl_booking_services.objects.filter(booking=booking)
    worknote = tbl_workedescription.objects.filter(booking=booking)

    total_amount = services.aggregate(
        total=Sum('final_amount')
    )['total'] or 0

    return render(
        request,
        "User/Invoice.html",
        {
            'data': booking,
            'services': services,
            'worknote': worknote,
            'total': total_amount
        }
    )


def view_vehicle(request):
    if 'uid' not in request.session:
      return redirect("Guest:Login")
    else:
      vehicledata=tbl_vehicle.objects.filter(user=request.session['uid'])
      greeting=tbl_user.objects.get(id=request.session['uid'])
      return render(request,"User/MyVehicle.html",{'data':vehicledata,'greeting':greeting})



def del_vehicle(request,did):
   tbl_vehicle.objects.get(id=did).delete()
   return render(request,"User/MyVehicle.html",{'msg':"Vehicle Deleted"})


def logout(request):
   request.session.flush()
   return redirect("Guest:Login")



def breakdown_assist(request):
    if 'uid' not in request.session:
      return redirect("Guest:Login")
    else:

      districtdata=tbl_district.objects.all()
      greeting=tbl_user.objects.get(id=request.session['uid'])
      placedata=tbl_place.objects.all()
   
      if request.method=="POST":
         servicecenter=tbl_servicecenter.objects.filter(place=request.POST.get("sel_place"),servicecenter_status=1)
         return render(request,"User/ViewBreakdown.html",{'servicecenter':servicecenter})

      else:
         return render(request,"User/ViewBreakdown.html",{'districtdata':districtdata,'placedata':placedata,'greeting':greeting})




def breakdown_booking(request, sid):
    if 'uid' not in request.session:
        return redirect("Guest:Login")

    user = tbl_user.objects.get(id=request.session['uid'])
    greeting = user
    servicecenter = tbl_servicecenter.objects.get(id=sid)

    vehicle_data = tbl_vehicle.objects.filter(user=user)

    breakdown_services = tbl_servicecenter_breakdown_services.objects.filter(servicecenter=servicecenter)

    if request.method == "POST":
        complaint = request.POST.get("txt_complaint")
        vehicle = tbl_vehicle.objects.get(id=request.POST.get("sel_vehicle"))
        service_id = request.POST.get("sel_service")

        
        booking = tbl_breakdownassist.objects.create(
            breakdown_complaint=complaint,
            user=user,
            servicecenter=servicecenter,
            vehicle=vehicle
        )

       
        service = tbl_servicecenter_breakdown_services.objects.get(id=service_id)

      
        tbl_breakdown_booking_services.objects.create(
            booking=booking,
            servicecenter_breakdown_service=service,
            base_amount=service.base_amount,        
            extra_charge=Decimal('0.00'),
            final_amount=service.base_amount       
        )

        return render(request,"User/HomePage.html",{'msg': "Breakdown Assistance Booked Successfully"})

    return render(request,"User/BreakdownBooking.html",
        {
            'vehicle_data': vehicle_data,
            'breakdown_services': breakdown_services,
            'greeting': greeting
        }
    )



def breakdown_status(request):
     if 'uid' not in request.session:
        return redirect("Guest:Login")
     else:
        data = tbl_breakdown_booking_services.objects.filter(booking__user_id=request.session['uid']).order_by('-id')
        return render(request, "User/BreakdownStatus.html", {'data': data})








def breakdown_payment(request, bs_id):
    bs = tbl_breakdown_booking_services.objects.get(id=bs_id,booking__user_id=request.session['uid'])

    if not bs.billing_status:
        return redirect("User:breakdownstatus")

    if request.method == "POST":
        
        bs.payment_status = True
        bs.save()
        return redirect("User:breakdown_status")

    return render(request, "User/BreakdownPayment.html", {
        "service": bs
    })


def breakdown_invoice(request, bs_id):
     if 'uid' not in request.session:
        return redirect("Guest:Login")
     else:
        service = tbl_breakdown_booking_services.objects.select_related(
            "booking",
            "booking__user",
            "booking__servicecenter",
            "booking__technician",
            "servicecenter_breakdown_service__servicetype"
        ).get(id=bs_id)

        return render(request, "User/BreakdownInvoice.html", {
            "service": service
        })



def feedback(request, bid):
    
    booking = tbl_booking.objects.get( id=bid, user_id=request.session['uid'])

    greeting = tbl_user.objects.get(id=request.session['uid'])

    # prevent duplicate feedback (optional but good)
    if tbl_feedback.objects.filter(booking=booking).exists():
        return render(
            request,
            "User/HomePage.html",
            {'msg': "Feedback already submitted"}
        )

    if request.method == "POST":
        rating = request.POST.get("rating")
        feedback_content = request.POST.get("feedback_content")

        tbl_feedback.objects.create(
            booking=booking,
            user=greeting,
            servicecenter=booking.servicecenter,
            rating=rating,
            feedback_content=feedback_content
        )

        return render(
            request,
            "User/MyServiceRequest.html",
            {'msg': "Feedback Submitted Successfully"}
        )

    return render(
        request,
        "User/Feedback.html",
        {
            "booking": booking,
            'greeting': greeting
        }
    )



    

def edit_feedback(request, fid):
    feedback = tbl_feedback.objects.get(id=fid,user_id=request.session['uid'])

    if request.method == "POST":
        feedback.rating = request.POST.get("rating")
        feedback.feedback_content = request.POST.get("feedback_content")
        feedback.save()
        return redirect("User:myservicerequest")


def delete_feedback(request, fid):
    feedback = tbl_feedback.objects.get(
        id=fid,
        user_id=request.session['uid']
    )
    feedback.delete()
    return redirect("User:myservicerequest")



def service_history(request,vid):
     if 'uid' not in request.session:
        return redirect("Guest:Login")
     else:
        vehicle=tbl_vehicle.objects.get(id=vid,user_id=request.session['uid'])
        bookings=tbl_booking.objects.filter(vehicle=vehicle,booking_status=12).annotate(total_amount=Sum('tbl_booking_services__final_amount')).prefetch_related('tbl_booking_services_set').order_by('-booking_date')
        breakdowns=tbl_breakdownassist.objects.filter(vehicle=vehicle,breakdown_status=3).annotate(total_amount=Sum('tbl_breakdown_booking_services__final_amount')).prefetch_related('tbl_breakdown_booking_services_set__servicecenter_breakdown_service').order_by('-breakdown_date')
        context = {
            "vehicle": vehicle,
            "completed_services": bookings,
            "completed_breakdowns": breakdowns,
        }
        return render(request, "User/Servicehistory.html", context)



def breakdown_status_api(request):
    if 'uid' not in request.session:
        return JsonResponse({"error": "Unauthorized"}, status=403)
    else:
        data = tbl_breakdown_booking_services.objects.filter(booking__user_id=request.session['uid']).order_by('-id')

        response = []

        for i in data:
            response.append({
                "id": i.id,
                "status": i.booking.breakdown_status,
                "progress_step": i.progress_step,
                "technician": i.booking.technician.technician_name if i.booking.technician else "",
                "total_amount": i.final_amount,
                "billing_status": i.billing_status,
                "payment_status": i.payment_status,
                
                
            })


        return JsonResponse({"data": response})




def myservice_request_api(request):
    if 'uid' not in request.session:
         return JsonResponse({"data":[]})
    else:
        bookings=tbl_booking.objects.filter(user=request.session['uid']).order_by('-id')
        response=[]
        
        for b in bookings:
            response.append({
                "id": b.id,
                "status": b.booking_status,
                "invoice_url": reverse("User:invoice", args=[b.id]) if b.booking_status > 11 else None,
                "payment_url": reverse("User:payment", args=[b.id]) if b.booking_status == 11 else None,
                "feedback_given": hasattr(b, "feedback") and b.feedback is not None,
            })
        return JsonResponse({"data": response})
        