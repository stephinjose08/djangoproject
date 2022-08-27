
# import string
# from unittest import result
# from django.template.loader import render_to_string
# from weasyprint import HTML
# import tempfile

from asyncio.windows_events import NULL
from genericpath import exists
import os
from django.views.decorators.csrf import csrf_exempt 
from django.conf import settings
# from django.template.loader import render_to_string
# from weasyprint import HTML
# import tempfile
# from django.conf import settings
# os.add_dll_directory(r"C:\Program Files\GTK3-RuntimeWin64\lib")
# os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\lib\girepository-1.0")
from datetime import datetime 
import datetime
from http.client import responses
from operator import is_, is_not
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from itertools import count
from django.contrib import messages
from multiprocessing import context
from tokenize import Number
from xml.sax.handler import all_properties
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from .models import  order,orderproduct, payment,canceled_orders, returned_orders
from cart.views import _cart_ID
from product.models import product,price,media,user_address,coupons
from cart.models import Cart, cartItem
import random
from django.contrib import messages
# Create your views here.
@login_required(login_url="login")
def check_out(request,total=0,id=0,quantity=0,cart_items=None,number=0,tax=0,grand_total=0):
    if id==0:
        try:
            if request.user.is_authenticated:
                cart_items=cartItem.objects.filter(useID=request.user)
            else:
                cart=Cart.objects.get(cart_ID=_cart_ID(request))
                cart_items=cartItem.objects.filter(cart=cart)
            if cart_items:
                for cart_item in cart_items:

                    Price=product.objects.get(id=cart_item.Product.id)
                    
                    total+=Price.discount_price * cart_item.quantity
                    number+=1
                    quantity=cart_item.quantity
                
                tax=(2*total)/100
                grand_total=total+tax  
            else:
                
                messages.error(request,"cart is empty!")
                return redirect('/')
                
        except ObjectDoesNotExist :
            pass
        try:
            if user_address.objects.filter(user=request.user).exists():
                existing_user=user_address.objects.filter(user=request.user).last()
            else:
                existing_user=NULL
        except ObjectDoesNotExist :
            pass
        context={
                'buynow':False,
                'cart_items':cart_items,
                'totalprice':total,
                'count':number, 
                'tax':tax,
                'grand_total':grand_total,
                'existing_user':existing_user,
                    
        }
        
    
        request.session['coupon']=0
        request.session['buynow']=0
        request.session['buynow_id']=0
        return render(request,'checkout.html',context)
    else:
        buynow_product=product.objects.get(id=id)
        request.session['buynow_id']=id
        total=buynow_product.discount_price
        tax=(total*2)/100
        grand_total=total+tax
        try:
            if user_address.objects.filter(user=request.user).exists():
                existing_user=user_address.objects.filter(user=request.user).first()
            else:
                existing_user=NULL
        except ObjectDoesNotExist:
            pass
        
        context={
                'buynow':True,
                'buynow_product':buynow_product,
                'totalprice':total,
                'count':number, 
                'tax':tax,
                'grand_total':grand_total,
                'existing_user':existing_user,           
        }
        request.session['coupon']=0
        request.session['buynow']=buynow_product.id
        return render(request,'checkout.html',context) 
@login_required(login_url="login")
def placeorder(request):
    
    id=request.session.get('buynow_id')
    request.session.delete('buynow_id')
    if id !=0:
        
        if request.method=="POST":
                buynow_product=product.objects.get(id=id) 
                #cart_items=cartItem.objects.filter(useID=request.user)
                total=buynow_product.discount_price
                # for cart_item in cart_items:

                #         Price=product.objects.get(id=cart_item.Product.id)

                    
                #         total+=Price.discount_price * cart_item.quantity
                grand_total=0 
                offerrate=0
                amount_discounted=0 
                tax=0 
                f=False 
            
                offerrate=request.session.get('coupon')
                new_order=order()
                if offerrate==0:
                    tax=(2*total)/100
                    grand_total=total+tax 
                    
                else:     
                    offerrate=request.session.get('coupon')
                    amount_discounted=total*(offerrate/100)
                    total=total-amount_discounted
                    tax=(2*total)/100
                    grand_total=total+tax
                    f=True
                    new_order.couponaplied=offerrate
                    del request.session['coupon']
                    
                new_payment=payment.objects.create(
                        user=request.user,
                        payment_mode="COD",
                        amount_paid=grand_total,
                        status="pending",
                        
                    )
                new_payment.save()
                if not request.POST.get('check'):
                    if not user_address.objects.filter(user=request.user).exists():
                        messages.error(request,"no address added!")
                        return redirect('/')
                    
                    address=user_address.objects.filter(user=request.user).first()
                    new_order.user=address.user
                    new_order.fist_name=address.fist_name
                    new_order.last_name=address.last_name
                    new_order.email=address.email
                    new_order.phone=address.phone
                    new_order.addressline1=address.addressline1
                    new_order.addressline2=address.addressline2
                    new_order.city=address.city
                    new_order.state=address.state
                    new_order.country=address.country
                    new_order.zip_code=address.zip_code
                    new_order.payment_mode=new_payment
                
                    new_order.total_price=grand_total
                 
                    new_order.notes=request.POST.get('notes')
                    tracknumber=str(random.randint(1111111,9999999))+str(new_order.zip_code)
                    while(order.objects.filter(tracking_number=tracknumber)) is None:
                        tracknumber=str(random.randint(1111111,9999999))+str(new_order.zip_code)
                        
                    new_order.tracking_number=tracknumber
                    new_order.save()
                    
                    # orderitems=cartItem.objects.filter(useID=request.user)
                    # for orderitem in orderitems:
                    orderproduct.objects.create(
                            order=new_order,
                            user=request.user,
                            product=buynow_product,
                            price=buynow_product.discount_price,
                            quantity=1,
                            payment=new_payment
                        )
                    
                    # cartItem.objects.filter(useID=request.user).delete()
                    print("deleted and order placed")
                    messages.success(request,"order placed!")
                    
                    


                else:
                    print(request.POST.get('check'))
                    print(request.POST.get('tempphone'))
                    # new_order=order()
                    new_order.user=request.user
                    new_order.fist_name=request.POST.get('tempfname')
                    new_order.last_name=request.POST.get('templname')
                    new_order.email=request.POST.get('tempemail')
                    new_order.phone=request.POST.get('tempphone')
                    new_order.addressline1=request.POST.get('tempaddress1')
                    new_order.addressline2=request.POST.get('tempaddress2')
                    new_order.city=request.POST.get('tempc')
                    new_order.state=request.POST.get('temps')
                    new_order.country=request.POST.get('tempcountry')
                    new_order.zip_code=request.POST.get('tempz')
                    new_order.payment_mode=new_payment
                    new_order.order_for_others=True
                    new_order.total_price=grand_total
                
                    new_order.notes=request.POST.get('notes')
                    
                    useraddress=user_address(
                                user=request.user,
                                fist_name=request.POST.get('tempfname'),
                                last_name=request.POST.get('templname'),
                                email=request.POST.get('tempemail'),
                                phone=request.POST.get('tempphone'),
                                addressline1=request.POST.get('tempaddress1'),
                                addressline2=request.POST.get('tempaddress2'),
                                city=request.POST.get('tempc'),
                                state=request.POST.get('temps'),
                                country=request.POST.get('tempcountry'),
                                zip_code=request.POST.get('tempz'),  
                               
                            )
                    useraddress.save()
                    tracknumber=str(random.randint(1111111,9999999))+str(new_order.zip_code)
                    while(order.objects.filter(tracking_number=tracknumber)) is None:
                        tracknumber=str(random.randint(1111111,9999999))+str(new_order.zip_code)
                        
                    new_order.tracking_number=tracknumber
                    new_order.save()
                    
                    # orderitems=cartItem.objects.filter(useID=request.user)
                    # for orderitem in orderitems:
                    orderproduct.objects.create(
                            order=new_order,
                            user=request.user,
                            product=buynow_product,
                            price=buynow_product.discount_price,
                            quantity=1,
                            payment=new_payment
                        )
                    
                    
                    print("deleted and order placed")
        
                    
            
                # cartItem.objects.filter(useID=request.user).delete()
                # return render(request,'invoice.html',context)
                messages.success(request,"order placed!")
                return redirect(my_orders)







        #buy now product placeorder end
    else:
        if request.method=="POST":
            cart_items=cartItem.objects.filter(useID=request.user)
            total=0
            for cart_item in cart_items:

                    Price=product.objects.get(id=cart_item.Product.id)

                
                    total+=Price.discount_price * cart_item.quantity
            grand_total=0 
            offerrate=0
            amount_discounted=0 
            tax=0 
            f=False 
        
            offerrate=request.session['coupon']
            new_order=order()
            
            if offerrate==0:
                tax=(2*total)/100
                grand_total=total+tax 
                
            else:     
                # offerrate=request.session['coupon']
                amount_discounted=total*(offerrate/100)
                total=total-amount_discounted
                tax=(2*total)/100
                grand_total=total+tax
                f=True
                new_order.couponaplied=offerrate
                del request.session['coupon']
                
            new_payment=payment.objects.create(
                    user=request.user,
                    payment_mode="COD",
                    amount_paid=grand_total,
                    status="pending",
                    
                )
            new_payment.save()
            if not request.POST.get('check'):
                if not user_address.objects.filter(user=request.user).exists():
                        messages.error(request,"no address added!")
                        return redirect('/')
                
                      
                address=user_address.objects.filter(user=request.user).first()
                new_order.user=address.user
                new_order.fist_name=address.fist_name
                new_order.last_name=address.last_name
                new_order.email=address.email
                new_order.phone=address.phone
                new_order.addressline1=address.addressline1
                new_order.addressline2=address.addressline2
                new_order.city=address.city
                new_order.state=address.state
                new_order.country=address.country
                new_order.zip_code=address.zip_code
                new_order.payment_mode=new_payment
            
                new_order.total_price=grand_total
         
                new_order.notes=request.POST.get('notes')
                tracknumber=str(random.randint(1111111,9999999))+str(new_order.zip_code)
                while(order.objects.filter(tracking_number=tracknumber)) is None:
                    tracknumber=str(random.randint(1111111,9999999))+str(new_order.zip_code)
                    
                new_order.tracking_number=tracknumber
                new_order.save()
                
                orderitems=cartItem.objects.filter(useID=request.user)
                for orderitem in orderitems:
                    orderproduct.objects.create(
                        order=new_order,
                        user=request.user,
                        product=orderitem.Product,
                        price=orderitem.Product.discount_price,
                        quantity=orderitem.quantity,
                        payment=new_payment
                    )
                
                cartItem.objects.filter(useID=request.user).delete()
                print("deleted and order placed")
                messages.success(request,"order placed!")
                
                


            else:
                print(request.POST.get('check'))
                print(request.POST.get('tempphone'))
                # new_order=order()
                new_order.user=request.user
                new_order.fist_name=request.POST.get('tempfname')
                new_order.last_name=request.POST.get('templname')
                new_order.email=request.POST.get('tempemail')
                new_order.phone=request.POST.get('tempphone')
                new_order.addressline1=request.POST.get('tempaddress1')
                new_order.addressline2=request.POST.get('tempaddress2')
                new_order.city=request.POST.get('tempc')
                new_order.state=request.POST.get('temps')
                new_order.country=request.POST.get('tempcountry')
                new_order.zip_code=request.POST.get('tempz')
                new_order.payment_mode=new_payment
                new_order.order_for_others=True
                new_order.total_price=grand_total
         
                new_order.notes=request.POST.get('notes')
                if  request.POST.get('checkbox'):
                    print("haiiiiiiii")
                    
                    useraddress=user_address(
                                user=request.user,
                                fist_name=request.POST.get('tempfname'),
                                last_name=request.POST.get('templname'),
                                email=request.POST.get('tempemail'),
                                phone=request.POST.get('tempphone'),
                                addressline1=request.POST.get('tempaddress1'),
                                addressline2=request.POST.get('tempaddress2'),
                                city=request.POST.get('tempc'),
                                state=request.POST.get('temps'),
                                country=request.POST.get('tempcountry'),
                                zip_code=request.POST.get('tempz'),  
                                
                            )
                    useraddress.save()
                tracknumber=str(random.randint(1111111,9999999))+str(new_order.zip_code)
                while(order.objects.filter(tracking_number=tracknumber)) is None:
                    tracknumber=str(random.randint(1111111,9999999))+str(new_order.zip_code)
                    
                new_order.tracking_number=tracknumber
                new_order.save()
                
                orderitems=cartItem.objects.filter(useID=request.user)
                for orderitem in orderitems:
                    orderproduct.objects.create(
                        order=new_order,
                        user=request.user,
                        product=orderitem.Product,
                        price=orderitem.Product.discount_price,
                        quantity=orderitem.quantity,
                        payment=new_payment
                    )
                
                
                print("deleted and order placed")
    
                
           
            cartItem.objects.filter(useID=request.user).delete()
            # return render(request,'invoice.html',context)
            messages.success(request,"order placed!")
            return redirect(my_orders)
@login_required(login_url="login")
def proced_to_pay(request):
    id=request.session.get('buynow_id')
    request.session.delete('buynow_id')
    
    if id !=0:
        buynow_product=product.objects.get(id=id) 
         
        total=0         
        #cart_items=cartItem.objects.filter(useID=request.user)
        total=buynow_product.discount_price
        # cart_items=cartItem.objects.filter(useID=request.user)   
          
        # for cart_item in cart_items:

        #             Price=product.objects.get(id=cart_item.Product.id)

                
        #             total+=Price.discount_price * cart_item.quantity
                
                    
        grand_total=0
        offerrate=0
        amount_discounted=0
        print("ivide")
        
        print(request.session.get('coupon'))
        print("thanne")
        offerrate=request.session['coupon']
        if offerrate==0:
            tax=(2*total)/100   
            grand_total=total+tax 
            
        else:
            print("coupon kandu")
            
            offerrate=request.session['coupon']
            amount_discounted=total*(offerrate/100)
            print(amount_discounted)
            total=total-amount_discounted
            tax=(2*total)/100
            grand_total=total+tax
            print(grand_total)
            # request.session.delete('coupon')
            # del request.session['coupon']
        return JsonResponse({
            'total_price':grand_total
        })
#buy now session



    else:
        cart_items=cartItem.objects.filter(useID=request.user)   
        total=0   
        for cart_item in cart_items:

                    Price=product.objects.get(id=cart_item.Product.id)

                
                    total+=Price.discount_price * cart_item.quantity
                
                    
        grand_total=0
        offerrate=0
        amount_discounted=0
        print("ivide")
        
        print(request.session['coupon'])
        print("thanne")
        offerrate=request.session['coupon']
        if offerrate==0:
            tax=(2*total)/100   
            grand_total=total+tax 
            
        else:
            print("coupon kandu")
            
            offerrate=request.session['coupon']
            amount_discounted=total*(offerrate/100)
            print(amount_discounted)
            total=total-amount_discounted
            tax=(2*total)/100
            grand_total=total+tax
            print(grand_total)
            # request.session.delete('coupon')
            # del request.session['coupon']
        return JsonResponse({
            'total_price':grand_total
        })
@login_required(login_url="login")
def online(request):
    id=request.session.get('buynow_id')
    request.session.delete('buynow_id')
    if id!=0:
        buynow_product=product.objects.get(id=id) 
        if request.method=="POST":
            # cart_items=cartItem.objects.filter(useID=request.user)
            total=0
            # for cart_item in cart_items:

            #             Price=product.objects.get(id=cart_item.Product.id)

                    
            #             total+=Price.discount_price * cart_item.quantity
                    
            total=buynow_product.discount_price          
            grand_total=0
            offerrate=0
            amount_discounted=0
            f=False
            # tax=(2*total)/100
            # grand_total=total+tax 
            new_order=order()
            offerrate=request.session['coupon']
            
            if offerrate==0:
                tax=(2*total)/100   
                grand_total=total+tax
                
            else:
                # offerrate=request.session.get('coupon')
                print(offerrate)
                amount_discounted=(offerrate/100)*total
                print(amount_discounted)
                f=True
                total=total-amount_discounted
                tax=(2*total)/100
                grand_total=total+tax
                new_order.couponaplied=offerrate
                del request.session['coupon']


            new_payment=payment.objects.create(
                        user=request.user,
                        payment_mode=request.POST.get('paymentmode'),
                        amount_paid=grand_total,
                        status="pending",
                        payment_id=request.POST.get('payment_id')
                        
                    )
            new_payment.save()
            

            if not request.POST.get('check'):
                    
                    address=user_address.objects.filter(user=request.user).first()
                    new_order.user=address.user
                    new_order.fist_name=address.fist_name
                    new_order.last_name=address.last_name
                    new_order.email=address.email
                    new_order.phone=address.phone
                    new_order.addressline1=address.addressline1
                    new_order.addressline2=address.addressline2
                    new_order.city=address.city
                    new_order.state=address.state
                    new_order.country=address.country
                    new_order.zip_code=address.zip_code
                    new_order.payment_mode=new_payment
                    print(request.POST.get('check'))
                    new_order.order_for_others=False
                    new_order.total_price=grand_total
                    
                    new_order.notes=request.POST.get('notes')
                    tracknumber=str(random.randint(1111111,9999999))+str(new_order.zip_code)
                    while(order.objects.filter(tracking_number=tracknumber)) is None:
                        tracknumber=str(random.randint(1111111,9999999))+str(new_order.zip_code)
                        
                    new_order.tracking_number=tracknumber
                    new_order.save()
                    
                    # orderitems=cartItem.objects.filter(useID=request.user)
                    # for orderitem in orderitems:
                    orderproduct.objects.create(
                            order=new_order,
                            user=request.user,
                            product=buynow_product,
                            price=buynow_product.discount_price,
                            quantity=1,
                            payment=new_payment
                        )
                    
                    # cartItem.objects.filter(useID=request.user).delete()
            else:
                print(request.POST.get('check'))
                print(request.POST.get('tempphone'))
                # new_order=order()              
                                    # csrfmiddlewaretoken : token,
                new_order.user=request.user
                new_order.fist_name=request.POST.get('first_name')
                new_order.last_name=request.POST.get('last_name')
                new_order.email=request.POST.get('email')
                new_order.phone=request.POST.get('phone')
                new_order.addressline1=request.POST.get('address1')
                new_order.addressline2=request.POST.get('address2')
                new_order.city=request.POST.get('city')
                new_order.state=request.POST.get('state')
                new_order.country=request.POST.get('country')
                new_order.zip_code=request.POST.get('zip')
                new_order.payment_mode=new_payment
                new_order.order_for_others=True
                new_order.total_price=grand_total
            
                new_order.notes=request.POST.get('notes')
                tracknumber=str(random.randint(1111111,9999999))+str(new_order.zip_code)
                while(order.objects.filter(tracking_number=tracknumber)) is None:
                    tracknumber=str(random.randint(1111111,9999999))+str(new_order.zip_code)
                    
                new_order.tracking_number=tracknumber
                new_order.save()
                
                # orderitems=cartItem.objects.filter(useID=request.user)
                # for orderitem in orderitems:
                orderproduct.objects.create(
                        order=new_order,
                        user=request.user,
                        product=buynow_product,
                        price=buynow_product.discount_price,
                        quantity=1,
                        payment=new_payment
                    )
                
                # cartItem.objects.filter(useID=request.user).delete()
                print("deleted and order placed")
            
        paymode=request.POST.get("paymentmode")
        print(paymode)
        if (paymode=="razorpay" or paymode=="paypal"):
            return JsonResponse({"status":'payment done',"buynow":'true',"id":id })
        else:
                print("havoooooo")
        
        # cartItem.objects.filter(useID=request.user).delete()
    
        return redirect(my_orders)



#end buy now session
    else:
        if request.method=="POST":
            cart_items=cartItem.objects.filter(useID=request.user)
            total=0
            for cart_item in cart_items:

                        Price=product.objects.get(id=cart_item.Product.id)

                    
                        total+=Price.discount_price * cart_item.quantity
                    
                        
            grand_total=0
            offerrate=0
            amount_discounted=0
            f=False
            # tax=(2*total)/100
            # grand_total=total+tax 
            new_order=order()
            offerrate=request.session['coupon']

            
            if offerrate==0:
                tax=(2*total)/100   
                grand_total=total+tax
                
            else:
                offerrate=request.session['coupon']
                amount_discounted=total*(offerrate/100)
                f=True
                total=total-amount_discounted
                tax=(2*total)/100
                grand_total=total+tax
                new_order.couponaplied=offerrate
                del request.session['coupon']


            new_payment=payment.objects.create(
                        user=request.user,
                        payment_mode=request.POST.get('paymentmode'),
                        amount_paid=grand_total,
                        status="pending",
                        payment_id=request.POST.get('payment_id')
                        
                    )
            new_payment.save()
            

            if not request.POST.get('check'):
                
                address=user_address.objects.filter(user=request.user).first()
                new_order.user=address.user
                new_order.fist_name=address.fist_name
                new_order.last_name=address.last_name
                new_order.email=address.email
                new_order.phone=address.phone
                new_order.addressline1=address.addressline1
                new_order.addressline2=address.addressline2
                new_order.city=address.city
                new_order.state=address.state
                new_order.country=address.country
                new_order.zip_code=address.zip_code
                new_order.payment_mode=new_payment
                print(request.POST.get('check'))
                new_order.order_for_others=False
                new_order.total_price=grand_total
                    
                new_order.notes=request.POST.get('notes')
                tracknumber=str(random.randint(1111111,9999999))+str(new_order.zip_code)
                while(order.objects.filter(tracking_number=tracknumber)) is None:
                    tracknumber=str(random.randint(1111111,9999999))+str(new_order.zip_code)
                        
                new_order.tracking_number=tracknumber
                new_order.save()
                    
                orderitems=cartItem.objects.filter(useID=request.user)
                for orderitem in orderitems:
                    orderproduct.objects.create(
                            order=new_order,
                            user=request.user,
                            product=orderitem.Product,
                            price=orderitem.Product.discount_price,
                            quantity=orderitem.quantity,
                            payment=new_payment
                        )
                    
                cartItem.objects.filter(useID=request.user).delete()
            else:
                print(request.POST.get('check'))
                print(request.POST.get('tempphone'))
                # new_order=order()              
                                    # csrfmiddlewaretoken : token,
                new_order.user=request.user
                new_order.fist_name=request.POST.get('first_name')
                new_order.last_name=request.POST.get('last_name')
                new_order.email=request.POST.get('email')
                new_order.phone=request.POST.get('phone')
                new_order.addressline1=request.POST.get('address1')
                new_order.addressline2=request.POST.get('address2')
                new_order.city=request.POST.get('city')
                new_order.state=request.POST.get('state')
                new_order.country=request.POST.get('country')
                new_order.zip_code=request.POST.get('zip')
                new_order.payment_mode=new_payment
                new_order.order_for_others=True
                new_order.total_price=grand_total
            
                new_order.notes=request.POST.get('notes')
                tracknumber=str(random.randint(1111111,9999999))+str(new_order.zip_code)
                while(order.objects.filter(tracking_number=tracknumber)) is None:
                    tracknumber=str(random.randint(1111111,9999999))+str(new_order.zip_code)
                    
                new_order.tracking_number=tracknumber
                new_order.save()
                
                orderitems=cartItem.objects.filter(useID=request.user)
                for orderitem in orderitems:
                    orderproduct.objects.create(
                        order=new_order,
                        user=request.user,
                        product=orderitem.Product,
                        price=orderitem.Product.discount_price,
                        quantity=orderitem.quantity,
                        payment=new_payment
                    )
                
                cartItem.objects.filter(useID=request.user).delete()
                print("deleted and order placed")
            
            paymode=request.POST.get("paymentmode")
            print(paymode)
            if (paymode=="razorpay" or paymode=="paypal"):
                return JsonResponse({"status":'payment done' })
            else:
                    print("havoooooo")
            
            cartItem.objects.filter(useID=request.user).delete()
        
            return redirect(my_orders) 

            
@login_required(login_url="login")
def my_orders(request,id=0):
   
        if order.objects.filter(user=request.user.id).exists():
            orders=order.objects.filter(user=request.user.id).order_by('-created_at')
            print(orders)
            print(request.user.id)
            orderedItems=orderproduct.objects.filter(order_id__in=orders)
            
            products=product.objects.filter(id__in=orderedItems)
            print(products)
            ziped_data=zip(orders,orderedItems,products)
            return render(request,'myorders.html',{"ziped_data":ziped_data,"orders":orders,"is_order":True})
        else:
            return render(request,'myorders.html',{"is_order":False})
@login_required(login_url="login")
def order_details(request,id):
    orderitems=orderproduct.objects.filter(order_id=id)
    userdetails=order.objects.get(id=id)
    return render(request,'detailorder.html',{"orderitems":orderitems,"userdetails":userdetails})
@login_required(login_url="login")   
def trackorder(request,track):
    result=order.objects.get(tracking_number=track)
    return render(request,'htmx/track.html',{"result":result})
@login_required(login_url="login")
def cancel_order(request,rack):
    
    canceled_order=order.objects.get(tracking_number=rack)
    print(rack)
    canceled_order.status="canceled"
    canceled_order.save()
    reason=request.POST.get("reason")
    print(reason)
    canceledorder=canceled_orders.objects.create(user=request.user,
                                                 order=canceled_order,
                                                 reason_for_cancel=reason)
    canceledorder.save()
    messages.success(request,"your order has canceled")
    return redirect(my_orders)
@login_required(login_url="login")
def return_order(request,rack):
    
    returned_order=order.objects.get(tracking_number=rack)
    print(rack)
    returned_order.status="returned"
    returned_order.save()
    reason=request.POST.get("reason")
    print(reason)
    returnorder=returned_orders.objects.create(user=request.user,
                                                 order=returned_order,
                                                 reason_for_return=reason)
    returnorder.save()
    messages.success(request,"your order has returned")
    return redirect(my_orders)
@login_required(login_url="login")
def coupenoffer(request):
    user=request.user
    f=False
    code=request.POST.get("code")
    print(code)
    print("helooo")
    id=request.session.get('buynow')
    print(id)
    # del request.session['buynow']

    #request.session.delete('buynow')
    # request.session['buynow_id']=id
    if id!=0:
        buynow_product=product.objects.get(id=id)
        total=0
        grand_total=0
        tax=0
        amount_discounted=0
        offerprice=0
        if coupons.objects.filter(couponcode=code).exists():
            coupon=coupons.objects.get(couponcode=code)
            print("coupon und")
            if coupons.objects.filter(couponcode=code,user_is_used=user).exists():
                print("keri")
                messages.error(request,"already used coupon")
                # for cart_item in cart_items:

                #     Price=product.objects.get(id=cart_item.Product.id)
                
                #     total+=Price.discount_price * cart_item.quantity
            
                total=buynow_product.discount_price 
                tax=(2*total)/100
                grand_total=total+tax  
                print(grand_total)
                print(tax)
                print(total)
        
                if user_address.objects.filter(user=request.user).exists():
                    existing_user=user_address.objects.filter(user=request.user).first()
                else:
                    existing_user=NULL
                context={
                'buynow':True,
                'buynow_product':buynow_product,
                'totalprice':total,
                'f':f,
                'tax':tax,
                'grand_total':grand_total,
                'existing_user':existing_user,       
                }
                print("used")
                request.session['coupon']=0
                return render(request,'htmx/offer.html',context)
                # request.session['coupon']=False     
            else:
                coupon.user_is_used.add(user)
                f=True
                coupon.save()
                
                
                # for cart_item in cart_items:

                #         Price=product.objects.get(id=cart_item.Product.id)

                    
                #         total+=Price.discount_price * cart_item.quantity
                    
                        
                total=buynow_product.discount_price
                offer=coupon.discount_percentage
                print(offer)
                amount_discounted=round(total*(offer/100),2)
                print(offerprice)
                
                offerprice=round(total-amount_discounted,2)
                print(offerprice)
                tax=round((2*offerprice)/100,2)
                grand_total=round(offerprice+tax,2)
                print(amount_discounted) 
                print("ivide thanne") 
                new_payment=payment.objects.create(
                        user=request.user,
                        
                        amount_paid=grand_total,
                        status="pending",
                        
                        
                    )
                new_payment.save()
                request.session['coupon']=offer
                print("coupon thazhe")
                print(request.session['coupon'])
                print("coupon mukalil")
                context={
                'buynow':True,
                'buynow_product':buynow_product,
                'totalprice':offerprice,
                'f':f,
                'tax':tax,
                'grand_total':grand_total,
                'amount_discounted':amount_discounted
                
                    
                }
                messages.error(request," coupon applied")
                return render(request,'htmx/offer.html',context)
        else:
            
            # for cart_item in cart_items:

            #     Price=product.objects.get(id=cart_item.Product.id)
                
            #     total+=Price.discount_price * cart_item.quantity
            
            total=buynow_product.discount_price
            tax=(2*total)/100
            grand_total=total+tax  
            print(grand_total)
            print(tax)
            print(total)
        
            if user_address.objects.filter(user=request.user).exists():
                existing_user=user_address.objects.filter(user=request.user).first()
            else:
                existing_user=NULL
            context={
                'buynow':True,
                'buynow_product':buynow_product,
                'totalprice':total,
                'f':f,
                'tax':tax,
                'grand_total':grand_total,
                'existing_user':existing_user,
                    
                }
            # request.session['coupon']=False
            request.session['coupon']=0
            messages.error(request,"invalid coupon")
            
            return render(request,'htmx/offer.html',context)
                                                                # buynow product coupon section end
    else:




        cart_items=cartItem.objects.filter(useID=request.user)
        total=0
        grand_total=0
        tax=0
        amount_discounted=0
        offerprice=0
        if coupons.objects.filter(couponcode=code).exists():
            coupon=coupons.objects.get(couponcode=code)
            print("coupon und")
            if coupons.objects.filter(couponcode=code,user_is_used=user).exists():
                print("keri")
                messages.error(request,"already used coupon")
                for cart_item in cart_items:

                    Price=product.objects.get(id=cart_item.Product.id)
                
                    total+=Price.discount_price * cart_item.quantity
            
            
                tax=(2*total)/100
                grand_total=total+tax  
                print(grand_total)
                print(tax)
                print(total)
        
                if user_address.objects.filter(user=request.user).exists():
                    existing_user=user_address.objects.filter(user=request.user).first()
                else:
                    existing_user=NULL
                context={
                'cart_items':cart_items,
                'totalprice':total,
                'f':f,
                'tax':tax,
                'grand_total':grand_total,
                'existing_user':existing_user,       
                }
                print("used")
                request.session['coupon']=0
                return render(request,'htmx/offer.html',context)
                # request.session['coupon']=False     
            else:
                coupon.user_is_used.add(user)
                f=True
                coupon.save()
                
                
                for cart_item in cart_items:

                        Price=product.objects.get(id=cart_item.Product.id)

                    
                        total+=Price.discount_price * cart_item.quantity
                    
                        
                
                offer=coupon.discount_percentage
                print(offer)
                amount_discounted=round(total*(offer/100),2)
                print(offerprice)
                
                offerprice=round(total-amount_discounted,2)
                print(offerprice)
                tax=round((2*offerprice)/100,2)
                grand_total=round(offerprice+tax,2)
                print(amount_discounted) 
                print("ivide thanne") 
                new_payment=payment.objects.create(
                        user=request.user,
                        
                        amount_paid=grand_total,
                        status="pending",
                        
                        
                    )
                new_payment.save()
                request.session['coupon']=offer
                print("coupon thazhe")
                print(request.session['coupon'])
                print("coupon mukalil")
                context={
                'cart_items':cart_items,
                'totalprice':offerprice,
                'f':f,
                'tax':tax,
                'grand_total':grand_total,
                'amount_discounted':amount_discounted
                
                    
                }
                return render(request,'htmx/offer.html',context)
        else:
            
            for cart_item in cart_items:

                Price=product.objects.get(id=cart_item.Product.id)
                
                total+=Price.discount_price * cart_item.quantity
            
            
            tax=(2*total)/100
            grand_total=total+tax  
            print(grand_total)
            print(tax)
            print(total)
        
            if user_address.objects.filter(user=request.user).exists():
                    existing_user=user_address.objects.filter(user=request.user).first()
            else:
                    existing_user=NULL
            context={
                'cart_items':cart_items,
                'totalprice':total,
                'f':f,
                'tax':tax,
                'grand_total':grand_total,
                'existing_user':existing_user,
                    
                }
            # request.session['coupon']=False
            request.session['coupon']=0
            messages.error(request,"invalid coupon")
            return render(request,'htmx/offer.html',context)
@login_required(login_url="login")        
def invoice(request,id):
    orders=order.objects.get(id=id)
    ordered_products=orderproduct.objects.filter(order_id=orders.id)
    total=0   
    for ordered_product in ordered_products:

                Price=product.objects.get(id=ordered_product.product_id)

            
                total+=Price.discount_price * ordered_product.quantity
             
                
    grand_total=0
    offerrate=0
    amount_discounted=0
    f=False

    offerrate=orders.couponaplied

    if offerrate is None:
        tax=(2*total)/100   
        grand_total=round(total+tax,2)
    else:
        # offerrate=request.session['coupon']
        f=True
        amount_discounted=round(total*(offerrate/100),2)
        print(amount_discounted)
        total=total-amount_discounted
        tax=(2*total)/100
        grand_total=round(total+tax,2)
        print(grand_total)
    # products=cartItem.objects.filter(useID=request.user)
    
    # request.session.delete('coupon')
    # cartItem.objects.filter(useID=request.user).delete()
    context= {'ordered_products':ordered_products,
            'orders':orders,
            'total':total,
            'tax':tax,
            'grand_total':grand_total,
            'f':f,
            'amount_discounted':amount_discounted
            }
    
    return render(request,'invoice.html',context)

# def pdf_view(request):

# def export_invoice_pdf(request):
#     response = HttpResponse(content_type = 'application/pdf')
#     response['Content-Disposition'] = 'inline; attachement; filename=Invoice' +'.pdf'

#     response['Content-Transfer-Encoding'] = 'binary'
#     orders=order.objects.get(id=1)
#     ordered_products=orderproduct.objects.filter(order_id=orders.id)
#     total=0   
#     for ordered_product in ordered_products:

#                 Price=product.objects.get(id=ordered_product.product_id)

            
#                 total+=Price.discount_price * ordered_product.quantity
             
                
#     grand_total=0
#     offerrate=0
#     amount_discounted=0
#     f=False

#     offerrate=orders.couponaplied

#     if offerrate is None:
#         tax=(2*total)/100   
#         grand_total=round(total+tax,2)
#     else:
       
#         f=True
#         amount_discounted=total*(offerrate/100)
#         print(amount_discounted)
#         total=total-amount_discounted
#         tax=(2*total)/100
#         grand_total=round(total+tax,2)
#         print(grand_total)
    
#     context= {'ordered_products':ordered_products,
#             'orders':orders,
#             'total':total,
#             'tax':tax,
#             'grand_total':grand_total,
#             'f':f,
#             'amount_discounted':amount_discounted
#             }
    

#     html_string = render_to_string('pdf.html',context)

#     html=HTML(string=html_string)

#     result = html.write_pdf()

#     with tempfile.NamedTemporaryFile(delete=True) as output : 
#         output.write(result)
#         output.flush()


#         output=open(output.name,'rb')

#         response.write(output.read())

#     return response












#     response=HttpResponse(content_type='application/pdf')
#     response['Content-Disposition']= 'inline; attachment; filename=invoice' +'.pdf'
#     #    str(datetime.datetime.now())
#     response['Content-Transfer-Encoding']='binary'

#     #order products query
#     orders=order.objects.get(id=1)
#     ordered_products=orderproduct.objects.filter(order_id=orders.id)
#     total=0   
#     for ordered_product in ordered_products:

#                 Price=product.objects.get(id=ordered_product.product_id)

            
#                 total+=Price.discount_price * ordered_product.quantity
             
                
#     grand_total=0
#     offerrate=0
#     amount_discounted=0
#     f=False

#     offerrate=orders.couponaplied

#     if offerrate is None:
#         tax=(2*total)/100   
#         grand_total=round(total+tax,2)
#     else:
       
#         f=True
#         amount_discounted=total*(offerrate/100)
#         print(amount_discounted)
#         total=total-amount_discounted
#         tax=(2*total)/100
#         grand_total=round(total+tax,2)
#         print(grand_total)
    
#     context= {'ordered_products':ordered_products,
#             'orders':orders,
#             'total':total,
#             'tax':tax,
#             'grand_total':grand_total,
#             'f':f,
#             'amount_discounted':amount_discounted
#             }
#     html_string=render_to_string('pdf.html',context)
#     page=HTML(string=html_string)
#     result=page.write_pdf()
#     with tempfile.NamedTemporaryFile(delete=True) as output:
#         output.write(result)
#         output.flush()
#         # output=output.seek(0)
#         output=open(output.name,'rb')
#         response.write(output.read())
#     return response

