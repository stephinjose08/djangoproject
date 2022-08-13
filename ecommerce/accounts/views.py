from ast import Return, arg
from audioop import reverse
from email import message
from multiprocessing import context
from turtle import home
from unicodedata import name
from unittest import result
from cart.models import cartItem,Cart
from cart.views import _cart_ID
from django.db.models import Sum

from orders.models import order,canceled_orders,orderproduct
from product.models import product,user_address
from django.contrib import messages
from twilio.rest import Client
from .models import user_address2
import re
import os
from telnetlib import AUTHENTICATION
from django.http import HttpResponse
from django.shortcuts import redirect,render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required






from .models import CustomUser, code
from .forms import codeVarification
from .utils import send_sms,check_sms
from product.models import banners,product,media,price,Category,brand
# Create your views here.
def userlogin(request):

    c_images=banners.objects.filter(discription='c_images')                                                    
    new_products=product.objects.filter(is_new_item=True)
    item_price=price.objects.filter(productItem_id__in=new_products.all())
    image=media.objects.filter(product_id__in=new_products.all())
    square_banner=banners.objects.get(discription='men-square_banner')
    last_image=banners.objects.get(discription='last_image')
    # second_banner=banners.objects.get(discription='womens_collection')
    # third_banner=banners.objects.get(discription='mens_new_arrival')
  
    # ziped_data=zip(new_products,item_price,list(image))

    

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

def auth_view(request):
    #form=AuthenticationForm()
    if request.method =='POST':
     
        phone=request.POST.get("phone")
        password=request.POST.get("password")
        
        user=authenticate(phone=phone,password=password)
        
        if user is not None:
            request.session['pk']=user.pk
            print("success")
            send_sms(user.phone)
            return render(request,'htmx/otp.html')
            # return redirect(sms_varification)
        else:
            print("incorrect")
    else:        
        return render(request,"login.html")
      
def sms_varification(request):
    pk=request.session.get("pk")
    user=CustomUser.objects.get(pk=pk)
    if request.method=="POST":
        print("entered")
    
    
        number=request.POST.get("otp")
        
        if check_sms(user,number)=='approved':

            try:
                cart=Cart.objects.get(cart_ID=_cart_ID(request))
                cart_item_exist=cartItem.objects.filter(cart=cart).exists()

                if cart_item_exist:
                     cart_items=cartItem.objects.filter(cart=cart)
                     cart_users=cartItem.objects.filter(useID=user)


                     for cart_item in cart_items:
                        f=0
                        # if cart_users:
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
                        # else:
                            # cart_item.user=user
                            # cart_item.save()

                        
            except:
                pass                                
            request.session['phone']=user.phone
            login(request,user)
            return redirect(userlogin)
        else:
            messages.error(request,"otp not correct")
            return redirect('/')
    # send_sms(user.phone)
    # return render(request,'loginvarification.html')   
    # return render(request,'htmx/otp.html')


def register(request):
  
        if request.method=='POST':
            
            request.session['firstname']=request.POST.get("first_name")

            request.session['lastname']=request.POST.get("last_name")  
            
            request.session['password']=request.POST.get("password") 
           
            request.session['email']=request.POST.get("email")

           
            
            request.session['phone']=request.POST.get("phone")
            print( request.session['email'])
            send_sms(request.session['phone'])
            return render(request,'htmx/signinotp.html')
            #return redirect(varify)  
        else:

            return render (request,'register.html')
    # 
            # user={
            #     'first_name':first_name,
            #     'last_name':last_name,
            #     'password':password,
            #     'email':email, 
            #     'phone':phone,
            # }
        #newuser=CustomUser.objects.create_user(first_name=first_name,last_name=last_name,email=email,phone=phone,password=password)
        #   reverse('newuservarify',kwargs={'first_name':first_name,
        #                                     'last_name':last_name,
        #                                     'password':password,
        #                                     'email':email, 
        #                                     'phone':phone})
           
        #newuser.save()
            
                 
        
    #  request.method=='POST':
    #         number=request.POST.get("varificationcode")
    #      check_sms(__phone__,number)=='approved':
    #             print(" data varified")
                # newuser=CustomUser.objects.create_user(first_name=__first_name__,last_name=__last_name__,email=__email__,phone=__phone__,password=__password__)
                #user=CustomUser.objects.create_user(first_name=user['first_name'],last_name=user['last_name'],email=user['email'],phone=user['phone'],password=user['password'])
                
                
            
        # messages.error(request,"otp not correct") 
        # send_sms(__phone__)
        # return render(request,'varification.html')      



# def home(request):
#     return render(request,'startpage.html')

def varify(request):
    if request.method=="POST":

        number=request.POST.get("otp")
        if check_sms(request.session['phone'],number)=='approved':
           print(" data varified")
           first_name=request.session['firstname']
           last_name=request.session['lastname']
           password=request.session['password']
           email=request.session['email'] 
           phone=request.session['phone']
           newuser=CustomUser.objects.create_user(first_name=first_name,last_name=last_name,email=email,phone=phone,password=password)
           newuser.save()
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
           request.session['phone']=phone
           login(request,newuser)
           return redirect(userlogin)
        else:
             messages.error(request,"otp not correct")
    else:
        send_sms(request.session['phone'])
        return render(request,'sign_invarification.html')      

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

    primary_address=user_address.objects.get(id=request.user.id)
    secondary_address=user_address2.objects.filter(user=request.user).first()
    ordercount=order.objects.filter(user=request.user).count()
    total_sum=order.objects.filter(user=request.user).aggregate(Sum('total_price'))['total_price__sum']
    total_sum=round(total_sum,2)
    latest_order=order.objects.filter(user=request.user).order_by('-created_at').exclude(status="canceled").first()
    latest_order_items=orderproduct.objects.filter(order_id=latest_order.id)
    canceled_order=canceled_orders.objects.filter(user=request.user).count()
    returned_count=order.objects.filter(user=request.user,status='returned').count()
    context={
            'primary_address':primary_address,
            'secondary_address':secondary_address,
            'ordercount':ordercount,'canceled_order':canceled_order,
            'total_sum':total_sum,
            'latest_order_items':latest_order_items,
            'latest_order':latest_order,
            'returned_count':returned_count,
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
    # context={
    #         'primary_address':primary_address,
    #         'secondary_address':secondary_address,
            
    # }
    return render(request,'htmx/change_address.html',{'primary_address':primary_address,'secondary_address':secondary_address})

