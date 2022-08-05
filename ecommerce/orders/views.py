from pyexpat.errors import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from itertools import count
from multiprocessing import context
from tokenize import Number
from xml.sax.handler import all_properties
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from .models import  order,orderproduct, payment
from cart.views import _cart_ID
from product.models import product,price,media,user_address
from cart.models import Cart, cartItem
import random
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
           

    return redirect(my_orders)

def proced_to_pay(request):
    cart_items=cartItem.objects.filter(useID=request.user)
    total=0   
    for cart_item in cart_items:

                Price=product.objects.get(id=cart_item.Product.id)

            
                total+=Price.discount_price * cart_item.quantity
             
                
    grand_total=0
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
        if paymode=="razorpay" or paymode=="paypal":
            JsonResponse({'status':"payment done"})
        else:
            print("havoooooo")
    return redirect(my_orders) 

            

def my_orders(request,id):
    orders=order.objects.filter(user=id)
    orderedItems=orderproduct.objects.filter(order_id__in=orders)
    products=product.objects.filter(id__in=orderedItems)
    ziped_data=zip(orders,orderedItems,products)
    return render(request,'myorders.html',{"ziped_data":ziped_data})

def test(request):
    if request.method=='POST':
        if not request.POST.get('check'):
            name=request.POST.get("fname")
        print(name)
    return render(request,'htmx/accordian.html')
    
