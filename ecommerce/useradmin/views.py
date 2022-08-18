from ast import Return
from asyncio.windows_events import NULL
from email.mime import image
from multiprocessing import context
from django.contrib import messages
from turtle import color
from unicodedata import category, name
from urllib.request import Request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from accounts.models import CustomUser
from django.contrib.auth import authenticate,login,logout

from django.db.models import Sum

from product.models import price,coupons
from orders.models import order,orderproduct,canceled_orders,payment
from django.contrib import messages

from product.models import brand, product,subcategory,media,Category,color,size,price,banners


# Create your views here.
def load_adminhome(request):
   COD=payment.objects.filter(payment_mode='COD').count()
   paypal=payment.objects.filter(payment_mode='paypal').count()
   razorpay=payment.objects.filter(payment_mode='razorpay').count()
   total_sum=order.objects.all().aggregate(Sum('total_price'))['total_price__sum']
   total_sum=round(total_sum,2)
   razorpay_total=payment.objects.filter(payment_mode='razorpay').aggregate(Sum('amount_paid'))['amount_paid__sum']
   razorpay_total=round(razorpay_total,2)
   paypal_total=payment.objects.filter(payment_mode='paypal').aggregate(Sum('amount_paid'))['amount_paid__sum']
   paypal_total=round(paypal_total,2)
   cod_total=payment.objects.filter(payment_mode='COD').aggregate(Sum('amount_paid'))['amount_paid__sum']
   cod_total=round(cod_total,2)
   menproducts=product.objects.filter(Category=Category.objects.get(name="MEN"))
   mensproducts=orderproduct.objects.filter(product__in=menproducts.all()).count()
   womenproducts=product.objects.filter(Category=Category.objects.get(name="WOMEN"))
   womensproducts=orderproduct.objects.filter(product__in=womenproducts.all()).count()
   kidproducts=product.objects.filter(Category=Category.objects.get(name="KIDS"))
   kidsproducts=orderproduct.objects.filter(product__in=kidproducts.all()).count()
   menproduct_count=product.objects.filter(Category=Category.objects.get(name="MEN")).count()
   womenproduct_count=product.objects.filter(Category=Category.objects.get(name="WOMEN")).count()
   kidproduct_count=product.objects.filter(Category=Category.objects.get(name="KIDS")).count()
   context={
    'COD':COD,
    'paypal':paypal,
    'razorpay':razorpay,
    'total_sum':total_sum,
    'razorpay_total':razorpay_total,
    'paypal_total':paypal_total,
    'cod_total':cod_total,
    'mensproducts':mensproducts,
    'womensproducts':womensproducts,
    'kidsproducts':kidsproducts,    
    'menproduct_count':menproduct_count,
    'kidproduct_count':kidproduct_count,
    'womenproduct_count':womenproduct_count,

   }
  
   return render(request,'accounting_dashboard.html',context)

def add_edit_categories(request,id=0):
    if id==0:
        if request.method=='POST':
            categoryname=request.POST.get('category')
            if Category.objects.filter(name=categoryname).exists():
                messages.error(request,"allready this category is here")
            new_category=Category(name=categoryname,categoryIcon=request.FILES['image'])
            new_category.save()
            return redirect(add_edit_categories)
        else:
            categories=Category.objects.all()
            return render(request,'add_edit_categories.html',{'categories':categories})
    else:
        if request.method=='POST':
            cat_name=request.POST.get('category')
            edited=Category.objects.get(id=id)
            edited.name=cat_name
            edited.categoryIcon=request.FILES['image']
            edited.save()
            return redirect(add_edit_categories)
        else:
            editing_category=Category.objects.get(id=id)
            categories=Category.objects.all()
            return render(request,'add_edit_categories.html',{'editing_category':editing_category,'categories':categories})  

def delete_category(request,id):
    deleted_category=Category.objects.get(id=id)
    deleted_category.delete()
    return redirect(add_edit_categories)




def add_edit_subcategories(request,id=0):
    if id==0:
        if request.method=='POST':
            subcategoryname=request.POST.get('subcategory')
            category=request.POST.get('main_category')
            print(category)
            new_category=subcategory(name=subcategoryname,maincategory=Category.objects.get(name=category),subcategoryIcon=request.FILES['image'])
            new_category.save()
            return redirect(add_edit_subcategories)
        else:
            categories=Category.objects.all()       
            subcategories=subcategory.objects.all()
            return render(request,'add_edit_subcategories.html',{'subcategories':subcategories,'categories':categories})
    else:
         if request.method=='POST':
            subcat_name=request.POST.get('subcategory')
            category=request.POST.get('main_category')

            edited=subcategory.objects.get(id=id)
            edited.name=subcat_name
            edited.maincatergory=Category.objects.get(name=category)
            edited.subcategoryIcon=request.FILES['image']
            edited.save()
            return redirect(add_edit_subcategories)
         else:
            editing_subcategory=subcategory.objects.get(id=id)
            subcategories=subcategory.objects.all()
            categories=Category.objects.all()
            return render(request,'add_edit_subcategories.html',{'editing_subcategory':editing_subcategory,'subcategories':subcategories,'categories':categories})  
 

def delete_subcategory(request,id):
    deleted_subcategory=subcategory.objects.get(id=id)
    deleted_subcategory.delete()
    return redirect(add_edit_subcategories)
def admin_login(request):
    
        if request.method=='POST':
            phone=request.POST.get('phone')
            password=request.POST.get('password')
            admin=authenticate(phone=phone,password=password)
            if admin is not None and admin.is_superuser:
                    request.session['phone']=phone
                    login(request,admin)
                    return redirect(load_adminhome)
            else:
                messages.error(request,"invalid username and password")
        return render(request,'adminlogin.html')
   


def log_out(request):
    if 'phone' in request.session:
        request.session.flush()
        logout(request) 
    return redirect(admin_login)

def displayUsers(request):
    users=CustomUser.objects.all()
    
    return render(request,"userview.html",{'users':users})
def block_user(request,id):
    
    
   
    blocked_user=CustomUser.objects.get(id=id)
    users=CustomUser.objects.all()
    if blocked_user.is_active:
        blocked_user.is_active=False
        blocked_user.save()
        messages.success(request,"user is blocked")
        # return render(request,'htmx/block_user.html',{'users':users})
    else:
        blocked_user.is_active=True
        blocked_user.save()
        messages.success(request,"user is unblocked")
    return render(request,'htmx/block_user.html',{'users':users})

    
    
    # messages.success(request,"user blocked")
    
    # return redirect(displayUsers)

def productlist(request):
    products=product.objects.all() 

    #prices=price.objects.all()
    #pr=prices.objects.all()
    #img=media.objects.all()
    category=Category.objects.all()
    Subcategory=subcategory.objects.all()
    # ziped_data=zip(products,category,Subcategory)
    return render(request,'ecommerce_product.html',{'products':products,'category':category,'Subcategory':Subcategory})


def add_OR_edit_Product(request,id=0):

    if id==0:
        if request.method=="POST":
            product_name=request.POST.get("name")
            product_title=request.POST.get("title")
            product_description=request.POST.get("description")
            category=request.POST.get("category")
            subCategory=request.POST.get("subcategory")
            Color=request.POST.get("color")
            Size=request.POST.get("size")
            actualprice=request.POST.get("orginalprice")
            discountrate=request.POST.get("discountrate")
            print(category)
            print(actualprice)
            print(discountrate)
            
            offerprice=request.POST.get("offerprice")
            print(offerprice)
            Brand=request.POST.get("brand")
            
            # if product_name=="":
            #     return HttpResponse("product name is empty")
            # elif len(product_name)<4:
            #     return HttpResponse("product name is too short")
            # elif not product_name.isalpha():
            #     return HttpResponse("product name only contains alphabets")

            # elif product_title=="":
            #      return HttpResponse("product title is not added")
            # elif len(product_title)<4:
            #     return HttpResponse("product title is too short")
            # elif not product_title.isalpha():
            #     return HttpResponse("product title only contains alphabets")
            
            # elif product_description=="":
            #      return HttpResponse("product discription is not added")
            # elif len(product_description)<10:
            #     return HttpResponse("product discription is too short")


            # elif  category=="":
            #     return HttpResponse("category not selected")

            # elif  subCategory=="":
            #     return HttpResponse("subcategory not selected")

            # elif  Brand=="":
            #     return HttpResponse("brand not selected")
            
            # elif  Color=="":
            #     return HttpResponse("color not selected")

            # elif  Size=="":
            #     return HttpResponse("size not selected")

            # elif  Size=="":
            #     return HttpResponse("size not selected")

            # elif  actualprice=="":
            #     return HttpResponse("orginal price  not added ")
            # elif not actualprice.isdigit():
            #     return HttpResponse("orginal price  only digits ")
            # elif  discountrate=="":
            #     return HttpResponse("discount rate  not selected")

            # elif  offerprice=="":
            #     return HttpResponse("offer price  not added ")
            # elif not offerprice.isdigit():
            #     return HttpResponse("offer price  only digits ")
          
           
            # if request.FILES['image1'] is None:
            #     return HttpResponse("add first image ")
            # elif request.FILES['image2'] is None:
            #     return HttpResponse("add second image ")
            # elif request.FILES['image3'] is None:
            #     return HttpResponse("add third image ")
            # elif request.FILES['image4'] is None:
            #     return HttpResponse("add second last image ")
            # elif request.FILES['image5'] is None:
            #     return HttpResponse("add last image ")
        
            new_product=product(
                                product_name=product_name,
                                product_title=product_title,
                                discription=product_description,
                                Category=Category.objects.get(name=category),
                                subcategory=subcategory.objects.get(name=subCategory),
                                color=color.objects.get(name=Color),
                                size=size.objects.get(name=Size),
                                brand=brand.objects.get(name=Brand),
                                actual_price=actualprice,
                                discount_price=offerprice,
                                discount_rate=discountrate,
                                cover_image=request.FILES['image1']
                                )
            new_product.save()
            addprice=price(
                            productItem=new_product,
                            actual_price=actualprice,
                            discount_price=offerprice,
                            discount_rate=discountrate
                            )
            addprice.save()
            
            
            Images=media(
                       product=new_product,
                        image1=request.FILES['image1'],
                        image2=request.FILES['image2'],
                        image3=request.FILES['image3'],
                        image4=request.FILES['image4'],
                        image5=request.FILES['image5']
                        )
            Images.save()
             
            # images=media(product=new_product,image1=image1,image2=image2,image3=image3,image4=image4,image5=image5)
            # images.save()
            return redirect(productlist)
        else:
            Brands=brand.objects.all()
            colors=color.objects.all()
            sizes=size.objects.all()
            categorys=Category.objects.all()
            subcategorys=subcategory.objects.all()
            return render(request,'addORedit.html' ,{'categorys':categorys,'subcategorys':subcategorys,'brands':Brands,'colors':colors,'sizes':sizes})
    else:
        if request.method=='POST':
            product_name=request.POST.get("name")
            product_title=request.POST.get("title")
            category=request.POST.get("category")
            Subcategory=request.POST.get("subcategory")
            Color=request.POST.get("color")
            Size=request.POST.get("size")
            actualprice=request.POST.get("orginalprice")
            discountrate=request.POST.get("discountrate")
            offerprice=request.POST.get("offerprice")
            Brand=request.POST.get("brand")
            
            products=product.objects.get(pk=id)
            
            products.product_name=product_name
            products.product_title=product_title                             
            products.category=Category.objects.get(name=category)                            
            products.subcategory=subcategory.objects.get(name=Subcategory)                              
            products.color=color.objects.get(name=Color)                             
            products.size=size.objects.get(name=Size)
            products.brand=brand.objects.get(name=Brand)
            products.actual_price=actualprice                               
            products.discount_rate=discountrate                              
            products.discount_price=offerprice 
            products.save()
            
            
            # products. image1=                            
            # products.  image2=                            
            # products.  image3=                             
            # products.  image4=                             
            # products. image5=                        

           
            # updated_price=price.objects.get(productItem=id) 
            # updated_price.productItem=products
            # updated_price.actual_price=actualprice                               
            # updated_price.discount_rate=discountrate                              
            # updated_price.discount_price=offerprice  

            # updated_price.save()
            
            
            return redirect(productlist)
        else:
            products=product.objects.get(pk=id)
            Brands=brand.objects.all()
            colors=color.objects.all()
            sizes=size.objects.all()
            categorys=Category.objects.all()
            subcategorys=subcategory.objects.all() 
            # updated_price=price.objects.get(productItem=id)  
            return render (request,'addORedit.html',{'product':products,'categorys':categorys,'subcategorys':subcategorys,'brands':Brands,'colors':colors,'sizes':sizes})

def deletproduct(request,id):
    deletproduct=product.objects.get(id=id)
    deletproduct.delete()
    products=product.objects.all()
    return render(request,'htmx/product_delet.html',{'products':products})
    # return redirect(productlist)

def baner_manage(request):
    banner=banners.objects.all()
    return render (request,'banners.html',{"banner":banner})

def orders(request):
    orders=order.objects.all().order_by('-created_at')
    cancel_orders=canceled_orders.objects.all().order_by('-cancel_date')
    return render(request,"orders.html" ,{'orders':orders,'cancel_orders':cancel_orders})

def subcategory_get(request):
    id=request.GET.get("Category")
    print(id)
    subcategorys=subcategory.objects.filter(maincategory=id)
    print(subcategorys)
    return render(request,'htmx/subcategory_htmx.html',{'subcategory':subcategorys})

def sort_by_category(request):
    id=request.GET.get("subcategory")
    if id==0:
        products=product.objects.all()
        return render(request,'htmx/product_delet.html',{'products':products})
    else:
        products=product.objects.filter(subcategory=id)
        return render(request,'htmx/product_delet.html',{'products':products})

def display_all(request):
    products=product.objects.all()
    return render(request,'htmx/product_delet.html',{'products':products})


def order_detail(request,id):
    orders=order.objects.get(id=id)
    print(orders)
    orderedproducts=orderproduct.objects.filter(order_id=id)
    products=product.objects.filter(id__in=orderedproducts)
    # print(orderedproducts[0].product_name)
    print(products)
    # ziped_data=zip(products,orderedproducts)
    return render(request,'order_details.html',{'orderedproducts':orderedproducts,'order':orders})

def delete_order(request,id):
    deleting_order=order.objects.get(id=id)
    deleting_order.delete()
    return redirect(orders)
   
def order_status_change(request,pid):
    update_order=order.objects.get(id=pid)
   
    status=request.POST.get("status")
    print(status)
    print(update_order)
    update_order.status=status
    update_order.save()
    return redirect(orders)



# def (request):
#     brands=brand.objects.all()
#     return render(request,'brands.html',{'brands':brands})

def brands(request,id=0):
    if id==0:
        if request.method=='POST':
            brand_name=request.POST.get('brand')
            
            new_brand=brand(name=brand_name,image=request.FILES['image'])
            new_brand.save()
            return redirect(brands)
        else:
            allbrand=brand.objects.all()
            return render(request,'brands.html',{'brands':allbrand})
    else:
        if request.method=='POST':
            updated_brand=request.POST.get('brand')
            edited=brand.objects.get(id=id)
            
            edited.name=updated_brand
            edited.image=request.FILES['image']
            edited.save()
            return redirect(brands)
        else:
            editing_brand=brand.objects.get(id=id)
            allbrand=brand.objects.all()
            return render(request,'brands.html',{'editing_brand':editing_brand,'brands':allbrand}) 

def delete_brand(request,id):
    deleting_brand=brand.objects.get(id=id)
    deleting_brand.delete()
    return redirect(brands)

# def couponadd(request):
#     coupon=coupons.objects.all()
#     return render(request,'coupon.html',{'coupons':coupon})

def couponadd(request,id=0):
    if id==0:
        if request.method=='POST':
            code=request.POST.get('code')
            discription=request.POST.get('discription')
            discount_rate=request.POST.get('rate')
            new_coupon=coupons(couponcode=code,discription=discription,discount_percentage=discount_rate)
            new_coupon.save()
            return redirect(couponadd)
        else:
            coupon=coupons.objects.all()
            return render(request,'coupon.html',{'coupon':coupon})
    else:
        if request.method=='POST':
            code=request.POST.get('code')
            discription=request.POST.get('discription')
            discount_rate=request.POST.get('rate')
            edited=coupons.objects.get(id=id)
            edited.couponcode=code
            edited.discription=discription    
            edited.discount_percentage=discount_rate         
            edited.save()
            return redirect(couponadd)
        else:
            editing_coupon=coupons.objects.get(id=id)
            coupon=coupons.objects.all()
            return render(request,'coupon.html',{'editing_coupon':editing_coupon,'coupon':coupon})

def category_offer(request,id=0):

    if id==0:
        if request.method=="POST":
            category=request.POST.get("categoryname")
            discount_rate=request.POST.get("discountrate")
            products=product.objects.filter(Category=Category.objects.get(name=category))

            for products in products:
                product_discount_rate=products.discount_rate
                if product_discount_rate<int(discount_rate):
                    products.discount_rate=int(discount_rate)
                    products.save()

            offer_name=request.POST.get("offername")
            category_obj=Category.objects.get(name=category)
            category_obj.offer=discount_rate
            category_obj.offer_name=offer_name
            category_obj.save()
            return redirect(category_offer)
        else:
            
            categories=Category.objects.all()
        return render(request,'category_offer.html',{'categories':categories})
    else:
        if request.method=="POST":
            category=request.POST.get("categoryname")
            discount_rate=request.POST.get("discountrate")
            category_obj=Category.objects.get(id=id)
            products=product.objects.filter(Category=Category.objects.get(name=category))
            for products in products:
                product_discount_rate=products.discount_rate
                if product_discount_rate<int(discount_rate):
                    products.discount_rate=int(discount_rate)
                    products.save()

            offer_name=request.POST.get("offername")
            category_obj=Category.objects.get(name=category)
            category_obj.offer=discount_rate
            category_obj.offer_name=offer_name
            category_obj.save()
            return redirect(category_offer)
        else:
            categories=Category.objects.all()
            category_obj=Category.objects.get(id=id)
            return render(request,'category_offer.html',{'categories':categories,'category_obj':category_obj})

def delete_category_offer(request,id):
    messages.warning(request," are you sure?")
    category_obj=Category.objects.get(id=id)
    category_obj.offer=NULL
    category_obj.offer_name=NULL
    category_obj.save()
    return redirect(category_offer)

def username_check(request):
    
    phone=request.POST.get("phone")
    if len(phone)<10:
        return HttpResponse("<p id='username-error' class='error'>phone number must contain 10 digits</p>")
    elif len(phone)>10:
        return HttpResponse("<p id='username-error' class='error'>phone number only contain 10 digits</p>")
    elif not phone.isdigit():
        return HttpResponse("<p id='username-error' class='error'>phone number may  only  numbers</p>")
    else:
        global usernamecheck
        usernamecheck=True
        return HttpResponse("<p id='username-error' class='text-success'>phone number is valid</p>")
    
def password_check(request):
    password=request.POST.get("password")


    if password=="":
        
        return HttpResponse("<p id='password-error' class='error'>password is not valid</p>")

    elif len(password)<4:
        return HttpResponse("<p id='password-error' class='error'>password is too short</p>")
    else:
       global passwordcheck
       passwordcheck=True
       return HttpResponse("<p id='password-error' class='success'>password is valid</p>") 