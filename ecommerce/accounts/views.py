from ast import Return, arg

from audioop import reverse
from email import message
import email
from multiprocessing import context

from unicodedata import name
from unittest import result
from urllib import request
from cart.models import cartItem,Cart
from cart.views import _cart_ID
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from orders.models import order,canceled_orders,orderproduct
from product.models import product,user_address
from django.contrib import messages
from twilio.rest import Client
from .models import user_address2
import re
import os
# from telnetlib import AUTHENTICATION
from django.http import HttpResponse
from django.shortcuts import redirect,render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.conf import settings





from .models import CustomUser, code
from .forms import codeVarification
from .utils import send_sms,check_sms
from product.models import banners,product,media,price,Category,brand
# Create your views here.
@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def userlogin(request):
    all_products=product.objects.all()
    for products in all_products:
        amount_discounted=products.actual_price*(products.discount_rate/100)
        products.discount_price=products.actual_price-amount_discounted
        products.save()

    for products in all_products:
        
        catoff=Category.objects.get(name=products.Category)
        if catoff.is_offer:
            if products.discount_rate<catoff.offer:
                products.discount_rate=catoff.offer
                amount_discounted=products.actual_price*(products.discount_rate/100)
                products.discount_price=products.actual_price-amount_discounted
        products.save()
    c_images=banners.objects.filter(discription='c_images')                                                    
    new_products=product.objects.filter(is_new_item=True)
    item_price=price.objects.filter(productItem_id__in=new_products.all())
    image=media.objects.filter(product_id__in=new_products.all())
    square_banner=banners.objects.get(discription='men-square_banner')
    last_image=banners.objects.get(discription='last_image')
    
    

    
    men_products=product.objects.filter(Category_id=Category.objects.get(name="MEN"))
    item_price=price.objects.filter(productItem_id__in=men_products.all())
    image=media.objects.filter(product_id__in=men_products.all())
    men_zip_data=zip(men_products,item_price,list(image))

    kids_products=product.objects.filter(Category_id=Category.objects.get(name="KIDS"))
    item_price=price.objects.filter(productItem_id__in=men_products.all())
    image=media.objects.filter(product_id__in=men_products.all())
    kids_zip_data=zip(kids_products,item_price,list(image))

    print(request.user)
    return render(request,'fasionhome.html', {'ziped_data':new_products,'c_images':c_images,'square_banner':square_banner,'last_image':last_image,'kids_zip_data':kids_zip_data})
@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def auth_view(request):
 
    if request.method =='POST':
     
        phone=request.POST.get("phone")
        password=request.POST.get("password")
        
        user=authenticate(phone=phone,password=password)
        
        if user is not None:
            request.session['pk']=user.pk
            print("success")
            
            return redirect(sms_varification)
        else:
            print("incorrect")
            messages.error(request,"username or password are incorrect")
            return render(request,"login.html")
        
    return render(request,"login.html")
        
@cache_control(no_cache =True, must_revalidate =True, no_store =True)     
def sms_varification(request):
    pk=request.session.get("pk")
    
    user=CustomUser.objects.get(pk=pk)
    print(user.phone)
    if request.method=="POST":
        print("entered")
    
    
        number=request.POST.get("otp")
        
        if check_sms(user,number)=='approved':
            request.session['phone']=user.phone
            try:
                cart=Cart.objects.get(cart_ID=_cart_ID(request))
                cart_item_exist=cartItem.objects.filter(cart=cart).exists()

                if cart_item_exist:
                     cart_items=cartItem.objects.filter(cart=cart)
                     cart_users=cartItem.objects.filter(useID=user)


                     for cart_item in cart_items:
                        f=0
                       
                        for cart_user in cart_users:
                                if cart_item.Product==cart_user.Product:
                                    cart_user.quantity+=cart_item.quantity
                                    cart_item.delete()
                                    cart_user.save()
                                    f=1
                                    break
                        if f==0:
                                    cart_item.useID=user
                                    cart_item.save()
                    

                        
            except:
                pass                                
            
            login(request,user)
            return redirect(userlogin)
        else:
            messages.error(request,"otp not correct")
            return render(request,'htmx/otp.html')
    else:
        send_sms(user.phone)
        return render(request,'htmx/otp.html')

@cache_control(no_cache =True, must_revalidate =True, no_store =True)     
def register(request):
  
        if request.method=='POST':
            
            request.session['firstname']=request.POST.get("first_name")

            request.session['lastname']=request.POST.get("last_name")  
            
            request.session['password']=request.POST.get("password") 
            if CustomUser.objects.filter(email=request.POST.get("email")).exists():
                messages.error(request,"this email already exists try another email")
                
                return render (request,'register.html')
           
            request.session['email']=request.POST.get("email")

           
            if CustomUser.objects.filter(phone=request.POST.get("phone")).exists():
                messages.error(request,"this user already exists try another phone number")
                return render (request,'register.html')
            request.session['phone']=request.POST.get("phone")
           
            phone=request.session['phone']
            
            return redirect(varify)
                #return redirect(varify)  
        else:

            return render (request,'register.html')
   
@cache_control(no_cache =True, must_revalidate =True, no_store =True)     
def varify(request):
    if request.method=="POST":

        number=request.POST.get("otp")
        print(number)
        if check_sms(request.session['phone'],number)=='approved':
            print(" data varified")
            first_name=request.session['firstname']
            last_name=request.session['lastname']
            password=request.session['password']
            email=request.session['email'] 
            phone=request.session['phone']
        
            newuser=CustomUser.objects.create_user(first_name=first_name,last_name=last_name,email=email,phone=phone,password=password)
            newuser.save()
            request.session['phone']=phone
            print("registration success")
            request.session.delete('firstname')
            request.session.delete('lastname')
            request.session.delete('password')
            request.session.delete('email') 
           
            try:
                cart=Cart.objects.get(cart_ID=_cart_ID(request))
                cart_item_exist=cartItem.objects.filter(cart=cart).exists()
                if cart_item_exist:
                    cart_items=cartItem.objects.filter(cart=cart)
                    
                    for cart_item in cart_items:
                        cart_item.user=newuser
                        cart_item.save()
                        # cart_user=cartItem(user=newuser,Product=cart_item.Product, quantity=cart_item.quantity)
                        # cart_item.delete()
                        # cart_user.save()
                        # # f=0
                        # for cart_user in cart_users:
                        #     if cart_item.Product==cart_user.Product:
                        #         cart_user.quantity+=cart_item.quantity
                        #         cart_item.delete()
                        #         cart_user.save()
                        #         f=1
                        #         break
                        #     if f==0:
                        #         cart_item.user=user
                        #         cart_item.save()
            except:
               pass
            
            login(request,newuser)
            return redirect(userlogin)
        else:
           messages.error(request,"otp not correct")
           print("not correct")
           return render(request,'htmx/signinotp.html')      

    else:
        send_sms(request.session['phone'])
        return render(request,'htmx/signinotp.html')      


def category_display(request,id):
    if id==1:
        products=product.objects.filter(Category_id=Category.objects.get(name="MEN"))[:8]
        item_price=price.objects.filter(productItem_id__in=products.all())
        image=media.objects.filter(product_id__in=products.all())
        # ziped_data=zip(products,item_price,list(image))

        return render (request,'htmx/nave.html',{'products':products})
    elif id==2:
        products=product.objects.filter(Category_id=Category.objects.get(name="WOMEN"))[:8]
        item_price=price.objects.filter(productItem_id__in=products.all())
        image=media.objects.filter(product_id__in=products.all())
        # ziped_data=zip(products,item_price,list(image))

        return render (request,'htmx/nave.html',{'products':products})

    elif id==3:
        products=product.objects.filter(Category_id=Category.objects.get(name="KIDS"))[:8]
        item_price=price.objects.filter(productItem_id__in=products.all())
        image=media.objects.filter(product_id__in=products.all())
        # ziped_data=zip(products,item_price,list(image))

        return render (request,'htmx/nave.html',{'products':products})
    elif id==4:
        brands=brand.objects.all()
        
        return render (request,'htmx/brand.html',{'brands':brands})
    else:
        return render(request,'pages_error404.html')


def log_out(request):
    if 'phone' in request.session:
        request.session.flush()
        logout(request) 
    return redirect(userlogin)


#htmx-url patterns

def username_check(request):
    
    phone=request.POST.get("phone")
    if len(phone)<10:
        return HttpResponse("<p id='username-error' class='error'>phone number must contain 10 digits</p>")
    elif len(phone)>10:
        return HttpResponse("<p id='username-error' class='error'>phone number only contain 10 digits</p>")
    elif not phone.isdigit():
        return HttpResponse("<p id='username-error' class='error'>phone number may  only  numbers</p>")

    return HttpResponse("<p id='username-error' class='success'>phone number is valid</p>")
    
def password_check(request):
    password=request.POST.get("password")


    if password=="":
        
        return HttpResponse("<p id='password-error' class='error'>password is not valid</p>")

    elif len(password)<4:
        return HttpResponse("<p id='password-error' class='error'>password is too short</p>")
    else:
       return HttpResponse("<p id='password-error' class='success'>password is valid</p>") 
    
       
def main_search(request):
    name=request.POST.get("search")
    
    results=product.objects.filter(product_title__icontains=name)
    if name=="":
        results=""

    return render(request,'htmx/searchresult.html',{'results':results})



@login_required(login_url="login")
def userprofile(request):
    ordercount=order.objects.filter(user=request.user).count()
    total_sum=order.objects.filter(user=request.user).aggregate(Sum('total_price'))['total_price__sum']
    if total_sum is not None:
        total_sum=round(total_sum,2)
    else:
        total_sum=0
   
    if user_address.objects.filter(user_id=request.user.id).exists():

            primary_address=user_address.objects.filter(phone=request.user).last()
            print(primary_address)
           
            secondary_address=user_address2.objects.filter(user=request.user).last()
            if order.objects.filter(user_id=request.user.id).exists():
                latest_order=order.objects.filter(user=request.user).order_by('-created_at').exclude(status="canceled").first()
                latest_order_items=orderproduct.objects.filter(order_id=latest_order.id)
                canceled_order=canceled_orders.objects.filter(user=request.user).count()
                returned_count=order.objects.filter(user=request.user,status='returned').count()
                username=CustomUser.objects.get(phone=request.user)
                context={
                'username':username,
                'primary_address':primary_address,
                'secondary_address':secondary_address,
                'ordercount':ordercount,'canceled_order':canceled_order,
                'total_sum':total_sum,
                'latest_order_items':latest_order_items,
                'latest_order':latest_order,
                'returned_count':returned_count,
                }
            else:
                context={
            'primary_address':primary_address,
            'secondary_address':secondary_address,
            'ordercount':0,'canceled_order':0,
            'total_sum':0,
            'latest_order_items':0,
            'latest_order':0,
            'returned_count':0,
        }

    else:
            context={
            'primary_address':None,
            'secondary_address':None,
            'ordercount':0,'canceled_order':0,
            'total_sum':0,
            'latest_order_items':0,
            'latest_order':0,
            'returned_count':0,
        }
   
    return render(request,'userprofile.html',context)

def add_to_primary(request):
    primary_address=user_address.objects.get(id=request.user.id)
    secondary_address=user_address2.objects.filter(user=request.user).first()
    fistname=primary_address.fist_name
    lastname=primary_address.last_name
    phone=primary_address.phone
    email=primary_address.email
    addressline1=primary_address.addressline1
    addressline2=primary_address.addressline2
    city=primary_address.city
    state=primary_address.state
    zip_code=primary_address.zip_code
    primary_address.fist_name=secondary_address.fist_name
    primary_address.last_name=secondary_address.last_name
    primary_address.phone=secondary_address.phone
    primary_address.email=secondary_address.email
    primary_address.addressline1=secondary_address.addressline1
    primary_address.addressline2=secondary_address.addressline2
    primary_address.city=secondary_address.city
    primary_address.state=secondary_address.state
    primary_address.zip_code=secondary_address.zip_code
    primary_address.save()
    secondary_address.fist_name=fistname    
    secondary_address.last_name=lastname
    secondary_address.phone=phone
    secondary_address.email=email
    secondary_address.addressline1=addressline1
    secondary_address.addressline2=addressline2
    secondary_address.city=city
    secondary_address.state=state
    secondary_address.zip_code=zip_code
    secondary_address.save()
  
    return render(request,'htmx/change_address.html',{'primary_address':primary_address,'secondary_address':secondary_address})
@login_required(login_url="login")
def add_new_address(request):
    if request.method=="POST":
        fist_name=request.POST.get("firstname")
        last_name=request.POST.get("lastname")
        phone=request.POST.get("phone")
        email=request.POST.get("email")
        addressline1=request.POST.get("addressline1")
        addressline2=request.POST.get("addressline2")
        city=request.POST.get("city")
        state=request.POST.get("state")
        zip_code=request.POST.get("zip")
        country=request.POST.get("country")
        if user_address.objects.filter(id=request.user.id).exists():

            user_address2(user_id =request.user.id,
                    fist_name=fist_name,
                    last_name=last_name,
                    phone=phone,
                    email=email,
                    addressline1=addressline1,
                    addressline2=addressline2,
                    city=city,
                    state=state,
                    zip_code=zip_code,
                    country=country
            ).save()
        else:
            newuser=CustomUser.objects.get(phone=request.user)
            user_address(user_id=newuser.id,
                    fist_name=fist_name,
                    last_name=last_name,
                    phone=phone,
                    email=email,
                    addressline1=addressline1,
                    addressline2=addressline2,
                    city=city,
                    state=state,
                    zip_code=zip_code,
                    country=country
            ).save()
        return render(request,'userprofile.html')
    else:
        return render(request,'htmx/add_newaddress.html')
