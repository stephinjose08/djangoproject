
from http.client import HTTPResponse
from itertools import count
from multiprocessing import context
from tokenize import Number
from urllib.request import Request
from xml.sax.handler import all_properties
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import wishlist
from django.urls import reverse
from django.contrib import messages
from product.models import product,price,media
from cart.models import Cart,cartItem
# Create your views here.

def _cart_ID(request):
    cart=request.session.session_key

    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,product_id):
    Product=product.objects.get(id=product_id)
    if Product.stock<1:
        messages.error(request,"product out of stok")
        return redirect('/')
    if request.user.is_authenticated:
        
        try:
            cartitems=cartItem.objects.get(Product=Product,useID=request.user)
            cartitems.quantity+=1
            print(cartitems)
            cartitems.save()
            print(cartitems)
        except:
            cartitems=cartItem.objects.create(
                Product=Product,
                useID=request.user,
                
                quantity=1
            )
            cartitems.save()
    else:
        try:
            cart=Cart.objects.get(cart_ID=_cart_ID(request)) #check cart id is present or not
        except Cart.DoesNotExist:

            cart=Cart.objects.create(cart_ID=_cart_ID(request)) #if not exist create one cart 
        cart.save() 

        try:
            cart_item=cartItem.objects.get(Product=Product,cart=cart) #is same product is in the cart then
            cart_item.quantity+=1
            cart_item.save()
        except cartItem.DoesNotExist:
            cart_item=cartItem.objects.create(Product=Product,quantity=1,cart=cart)
            cart_item.save()
    return redirect(cart_items)



def cart_items(request,total=0,quantity=0,cart_items=None,number=0,tax=0,grand_total=0):
    
    try:
        if request.user.is_authenticated:
            cart_items=cartItem.objects.filter(useID=request.user)
        else:
            cart=Cart.objects.get(cart_ID=_cart_ID(request))
            cart_items=cartItem.objects.filter(cart=cart)
            
        for cart_item in cart_items:

            # Price=price.objects.get(productItem=cart_item.Product)
            Price=product.objects.get(id=cart_item.Product.id)
            total+=Price.discount_price * cart_item.quantity
            number+=1
            quantity=cart_item.quantity

       
        tax=(2*total)/100
        grand_total=total+tax  
      
        
         
        
       

    except ObjectDoesNotExist :
        pass
       
    context={
            'cart_items':cart_items,
            'totalprice':total,
            'count':number, 
            'tax':tax,
            'grand_total':grand_total,
            
            
            
           
                
      }
    
   
    

  
    return render(request,'cart.html',context)

def remove_cart(request,product_id):
    Product=product.objects.get(id=product_id)
    total=0
    quantity=0
    cart_items=None
    number=0
    tax=0
    grand_total=0
    if  request.user.is_authenticated:
        # cart=Cart.objects.get(cart_ID=request.user)
        cartitem=cartItem.objects.get(Product=Product,useID=request.user)
        if cartitem.quantity>1:
            cartitem.quantity-=1
            cartitem.save()
        # else:
        #     cartitem.delete()
    else:

        cart=Cart.objects.get(cart_ID=_cart_ID(request))
    
        cartitem=cartItem.objects.get(Product=Product,cart=cart)
        if cartitem.quantity>1:
            cartitem.quantity-=1
            cartitem.save()
        # else:
        #     cartitem.delete()
    
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
       
    context={
            'cart_items':cart_items,
            'totalprice':total,
            'count':number, 
            'tax':tax,
            'grand_total':grand_total,
            
            
            
           
                
      }
    
    return render(request,"htmx/quantity_change.html",context)
    # return redirect(cart_items)

def add_product(request,product_id):
    Product=product.objects.get(id=product_id)
    total=0
    quantity=0
    cart_items=None
    number=0
    tax=0
    grand_total=0
    if  request.user.is_authenticated:
        # cart=Cart.objects.get(cart_ID=request.user)
        cartitem=cartItem.objects.get(Product=Product,useID=request.user)
        cartitem.quantity+=1
        cartitem.save() 
    else:
        cart=Cart.objects.get(cart_ID=_cart_ID(request))
        cartitem=cartItem.objects.get(Product=Product,cart=cart)
        cartitem.quantity+=1
        cartitem.save()
    # return redirect(cart_items)
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
       
    context={
            'cart_items':cart_items,
            'totalprice':total,
            'count':number, 
            'tax':tax,
            'grand_total':grand_total,
            
            
            
           
                
      }
    
    return render(request,"htmx/quantity_change.html",context)


def remove_cartitem(request,product_id):
    Product=product.objects.get(id=product_id)
    total=0
    quantity=0
    cart_items=None
    number=0
    tax=0
    grand_total=0
    if  request.user.is_authenticated:
       
        cartitem=cartItem.objects.get(Product=Product,useID=request.user)
        cartitem.delete()
    else:
        cart=Cart.objects.get(cart_ID=_cart_ID(request))
        cartitem=cartItem.objects.get(Product=Product,cart=cart)
        cartitem.delete()
    
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
       
    context={
            'cart_items':cart_items,
            'totalprice':total,
            'count':number, 
            'tax':tax,
            'grand_total':grand_total,     
                
      }
    
    return render(request,"htmx/quantity_change.html",context)
    # return redirect(cart_items)
@login_required(login_url="login")
def wishlist_page(request):
    wishlist_item=wishlist.objects.all()
    return render(request,'wishlist.html',{'wishlist_items':wishlist_item})


@login_required(login_url="login")
def add_to_wishlist(request,id):
    wishlist_item=product.objects.get(id=id)
    if wishlist.objects.filter(wishlist_items=wishlist_item).exists():
        messages.error(request,"already added into wishlist")
    else:
        wishlist(user_id=request.user,wishlist_items=wishlist_item).save()
    return redirect(wishlist_page)
@login_required(login_url="login")   
def remove_from_wishlist(request,id):
    deleting_item=wishlist.objects.get(user_id=request.user,wishlist_items=id)
    deleting_item.delete()
    wishlist_item=wishlist.objects.all()
    messages.success(request,"remove item successfully")
    return render(request,'htmx/remove_wishlist_item.html',{'wishlist_items':wishlist_item})



