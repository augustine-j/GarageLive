from django.shortcuts import render,redirect
from Guest.models import *

# Create your views here.

def homepage(request):
    sellerdata=tbl_seller.objects.get(id=request.session['sid'])
    return render(request,"Seller/HomePage.html",{'Data':sellerdata})


def profile(request):
    sellerdata=tbl_seller.objects.get(id=request.session['sid'])
    return render(request,"Seller/Profile.html",{'Data':sellerdata})

def editprofile(request):
    editprofile=tbl_seller.objects.get(id=request.session['sid'])
    if request.method=="POST":
        name=request.POST.get("txt_name")
        email=request.POST.get("txt_email")
        contact=request.POST.get("txt_contact")
        estd_date=request.POST.get("txt_date")
        license_number=request.POST.get("license_number")
        owner=request.POST.get("txt_owner")
        editprofile.user_name=name
        editprofile.user_email=email
        editprofile.contact_number=contact
        editprofile.estd_date=estd_date
        editprofile.license_number=license_number
        editprofile.owner_name=owner
        editprofile.save()
        return render(request,"Seller/Profile.html",{'msg':"Data Updated"})
    else:
        return render(request,"Seller/Editprofile.html",{'Data':editprofile})



def changepassword(request):
    sellerdata=tbl_seller.objects.get(id=request.session['sid'])
    dbpass=sellerdata.password
    if request.method=="POST":
        old=request.POST.get("txt_password")
        new=request.POST.get("new_password")
        confirm=request.POST.get("confirm_password")
        if old==dbpass:
            if new==confirm:
                sellerdata.password=new
                sellerdata.save()
                return render(request,"Seller/Profile.html",{'msg':"Password Updated"})
            else:
                return render(request,"Seller/ChangePassword.html",{'msg':"Invalid Password"})
        else:
            return render(request,"Seller/ChangePassword.html",{'msg':"Invalid Password"})

    else:
        return render(request,"Seller/ChangePassword.html",{'Data':sellerdata})