
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
from .models import  order,orderproduct, payment,canceled_orders
from cart.views import _cart_ID
from product.models import product,price,media,user_address,coupons
from cart.models import Cart, cartItem
import random
from django.contrib import messages
# Create your views here.
@login_required(login_url="login")
def check_out(request,total=0,quantity=0,cart_items=None,number=0,tax=0,grand_total=0):
    
    try:
        if request.user.is_authenticated:
            cart_items=cartItem.objects.filter(useID=request.user)
        else:
            cart=Cart.objects.get(cart_ID=_cart_ID(request))
            cart_items=cartItem.objects.filter(cart=cart)
    
        for cart_item in cart_items:

            Price=product.objects.get(id=cart_item.Product.id)
            
            total+=Price.discount_price * cart_item.quantity
            number+=1
            quantity=cart_item.quantity
        
        tax=(2*total)/100
        grand_total=total+tax  
        
    except ObjectDoesNotExist :
        pass
    if user_address.objects.get(user=request.user):
        existing_user=user_address.objects.get(user=request.user)
    context={
            'cart_items':cart_items,
            'totalprice':total,
            'count':number, 
            'tax':tax,
            'grand_total':grand_total,
            'existing_user':existing_user,
                
     }
    
  
    
    return render(request,'checkout.html',context)

def placeorder(request):
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
        if request.session['coupon']:
           
            offerrate=request.session['coupon']
            amount_discounted=total*(offerrate/100)
            total=total-amount_discounted
            tax=(2*total)/100
            grand_total=total+tax
            request.session.delete('coupon')   
        else:     
            
            tax=(2*total)/100
            grand_total=total+tax  
        new_payment=payment.objects.create(
                user=request.user,
                payment_mode="COD",
                amount_paid=grand_total,
                status="pending",
                
            )
        new_payment.save()
        if not request.POST.get('check'):
          
            new_order=order()
            address=user_address.objects.get(user=request.user)
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
            new_order.notes
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
            
            


        else:
            print(request.POST.get('check'))
            print(request.POST.get('tempphone'))
            new_order=order()
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
            new_order.notes
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
        return redirect(my_orders)

def proced_to_pay(request):
    cart_items=cartItem.objects.filter(useID=request.user)   
    total=0   
    for cart_item in cart_items:

                Price=product.objects.get(id=cart_item.Product.id)

            
                total+=Price.discount_price * cart_item.quantity
             
                
    grand_total=0
    offerrate=0
    amount_discounted=0
    if request.session['coupon']:
        print("coupon kandu")
        print(request.session['coupon'])
        offerrate=request.session['coupon']
        amount_discounted=total*(offerrate/100)
        print(amount_discounted)
        total=total-amount_discounted
        tax=(2*total)/100
        grand_total=total+tax
        print(grand_total)
        
    else:
        tax=(2*total)/100   
        grand_total=total+tax
    
    return JsonResponse({
        'total_price':grand_total
    })

def online(request):
    if request.method=="POST":
        cart_items=cartItem.objects.filter(useID=request.user)
        total=0
        for cart_item in cart_items:

                    Price=product.objects.get(id=cart_item.Product.id)

                
                    total+=Price.discount_price * cart_item.quantity
                
                    
        grand_total=0
        offerrate=0
        amount_discounted=0
        # tax=(2*total)/100
        # grand_total=total+tax 
        if request.session['coupon']:
            
            
            offerrate=request.session['coupon']
            amount_discounted=total*(offerrate/100)
            
            total=total-amount_discounted
            tax=(2*total)/100
            grand_total=total+tax
           
            request.session.delete('coupon')
        else:
            tax=(2*total)/100   
            grand_total=total+tax


        new_payment=payment.objects.create(
                    user=request.user,
                    payment_mode=request.POST.get('paymentmode'),
                    amount_paid=grand_total,
                    status="pending",
                    payment_id=request.POST.get('payment_id')
                    
                )
        new_payment.save()
        print(request.POST.get('zip'))

        if not request.POST.get('check'):
                new_order=order()
                address=user_address.objects.get(user=request.user)
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
            new_order=order()              
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
           return JsonResponse({"status":'payment done'})
    else:
            print("havoooooo")
    return redirect(my_orders) 

            

def my_orders(request):
    orders=order.objects.filter(user=request.user.id).order_by('created_at')
    orderedItems=orderproduct.objects.filter(order_id__in=orders)
    products=product.objects.filter(id__in=orderedItems)
    ziped_data=zip(orders,orderedItems,products)
    return render(request,'myorders.html',{"ziped_data":ziped_data})

def order_details(request,id):
    orderitems=orderproduct.objects.filter(order_id=id)
    userdetails=order.objects.get(id=id)
    return render(request,'detailorder.html',{"orderitems":orderitems,"userdetails":userdetails})
    
def trackorder(request,track):
    result=order.objects.get(tracking_number=track)
    return render(request,'htmx/track.html',{"result":result})

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
    return redirect(my_orders)

def coupenoffer(request):
    user=request.user
    f=False
    code=request.POST.get("code")
    print(code)
    print("helooo")
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
    
            if user_address.objects.get(user=request.user):
                existing_user=user_address.objects.get(user=request.user)
            context={
            'cart_items':cart_items,
            'totalprice':total,
             'f':f,
            'tax':tax,
            'grand_total':grand_total,
            'existing_user':existing_user,       
            }

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
            new_payment=payment.objects.create(
                    user=request.user,
                    
                    amount_paid=grand_total,
                    status="pending",
                    
                    
                )
            new_payment.save()
            request.session['coupon']=offer
        context={
            'cart_items':cart_items,
            'totalprice':total,
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
    
        if user_address.objects.get(user=request.user):
            existing_user=user_address.objects.get(user=request.user)
        context={
            'cart_items':cart_items,
            'totalprice':total,
            'f':f,
            'tax':tax,
            'grand_total':grand_total,
            'existing_user':existing_user,
                
            }
    
        
        messages.error(request,"invalid coupon")
        return render(request,'htmx/offer.html',context)
        

    
   



