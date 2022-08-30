

from datetime import date, datetime
from email.mime import image
# from genericpath import exists
from multiprocessing import context
# from re import search
from django.contrib import messages

from urllib.request import Request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from accounts.models import CustomUser
from django.contrib.auth import authenticate,login,logout
import csv
import xlwt
import os
# GTK_FOLDER=r'C:\Program Files\GTK3-Runtime Win64\bin'
# os.environ['PATH']=GTK_FOLDER + os.pathsep + os.environ.get('PATH','')
# from django.template.loader import render_to_string
# from weasyprint import HTML
# import tempfile
from django.views.decorators.cache import cache_control
from django.db.models import Sum
from datetime import date
from product.models import price,coupons
from orders.models import order,orderproduct,canceled_orders,payment
from django.contrib import messages

from product.models import brand, product,subcategory,media,Category,color,size,price,banners





# Create your views here.

@cache_control(no_cache =True, must_revalidate =True, no_store =True)  
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
                return redirect(add_edit_categories)
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

@cache_control(no_cache =True, must_revalidate =True, no_store =True)     
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
            product_description=request.POST.get("description")
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
            products.discription=product_description,                            
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
    if request.method=='POST':
        discription=request.POST.get("discription")
        banners(image=request.FILES['b_image'],discription=discription).save()
    
    banner=banners.objects.all()
    return render (request,'banners.html',{"banner":banner})
def banner_delete(request,id):
    banner_item=banners.objects.get(id=id)
    banner_item.delete()
    return redirect(baner_manage)

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
            if brand.objects.filter(name=brand_name).exists():
                messages.error(request,"allready this brand is here")
                return redirect(brands)
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
            if code=="":
                messages.error(request,"coupon code should not be empty")
                return redirect(couponadd)
            if coupons.objects.filter(couponcode=code).exists():
                messages.error(request,"coupon already exist")
                return redirect(couponadd)
            discription=request.POST.get('discription')
            discount_rate=request.POST.get('rate')
            if discount_rate=="":
                messages.error(request,"offer rate  should not be empty")
                return redirect(couponadd)
            if discount_rate>'70':
                messages.error(request,"maximum offer allowed  70%")
                return redirect(couponadd)
            new_coupon=coupons(couponcode=code,discription=discription,discount_percentage=discount_rate)
            new_coupon.save()
            messages.success(request," coupon added successfully")
            return redirect(couponadd)
        else:
            coupon=coupons.objects.all()
            return render(request,'coupon.html',{'coupon':coupon})
    else:
        if request.method=='POST':
            code=request.POST.get('code')
            if code=="":
                messages.error(request,"coupon code should not be empty")
                return redirect(couponadd)
            discription=request.POST.get('discription')
            discount_rate=request.POST.get('rate')
            if discount_rate>'70':
                messages.error(request,"maximum offer allowed  70%")
                return redirect(couponadd)
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

def coupon_delete(request,id):
    coupon=coupons.objects.get(id=id)
    coupon.delete()
    return redirect(couponadd)

def category_offer(request,id=0):

    if id==0:
        if request.method=="POST":
            category=request.POST.get("categoryname")
            discount_rate=request.POST.get("discountrate")
            if discount_rate=='100':
                messages.error(request,"not accept 100 % discount")
                return redirect(category_offer)
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
            category_obj.is_offer=True
            category_obj.save()
            return redirect(category_offer)
        else:
            
            categories=Category.objects.all()
        return render(request,'category_offer.html',{'categories':categories})
    else:
        if request.method=="POST":
            category=request.POST.get("categoryname")
            discount_rate=request.POST.get("discountrate")
            if discount_rate=='100':
                messages.error(request,"not accept 100 % discount")
                return redirect(category_offer)
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
    
    category_obj=Category.objects.get(id=id)
    category_obj.offer=None
    category_obj.offer_name=None
    category_obj.is_offer=False
    category_obj.save()
    messages.success(request," deleted successfully")
    return redirect(category_offer)

def product_offer_Add_Edit(request,id=0):
    if id==0:
       if request.method=="POST":
            product_id=request.POST.get("productid")
            discount_rate=request.POST.get("discountrate")
            if discount_rate>'70':
                messages.error(request,"not accept more than 70  % discount")
                return redirect(product_offer_Add_Edit)
            products=product.objects.get(id=product_id)

            products.discount_rate=int(discount_rate)
            products.save()
            return redirect(product_offer_Add_Edit)
       else:
            products=product.objects.all()
            return render(request,'product_offer.html',{'products':products})
    else:
        if request.method=="POST":
            product_id=request.POST.get("productid")
            if product_id=="":
               messages.error(request,"select product")
               return redirect(product_offer_Add_Edit) 

            print(product_id)
            discount_rate=request.POST.get("discountrate")
            if discount_rate>'70':
                messages.error(request,"not accept more than 70  % discount")
                return redirect(product_offer_Add_Edit)
            products=product.objects.get(id=product_id)
            products.discount_rate=int(discount_rate)
            products.save()
            return redirect(product_offer_Add_Edit)
        else:
            products=product.objects.all()
            return render(request,'product_offer.html',{'products':products})
def delete_product_offer(request,id):
    
    product_item=product.objects.get(id=id)
    product_item.discount_rate=0
   
    product_item.save()
    messages.success(request," deleted successfully")
    return redirect(product_offer_Add_Edit)


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
       return HttpResponse("<p id='password-error' class='text-success'>password is valid</p>") 

def sales_Report(request):
    delivered_products=order.objects.filter(status="delivered")
    number_of_success_orders=order.objects.filter(status="delivered").count()
    return render(request,'salesreport.html',{"delivered_products":delivered_products,'number_of_success_orders':number_of_success_orders})

def yearly_salesreport(request):

    year=request.POST.get("year")
    if year=='0':
      delivered_products=order.objects.filter(status="delivered")  
      return render(request,'htmx/sales_report_table.html',{'delivered_products':delivered_products})
    else:
        delivered_products=order.objects.filter(status="delivered",created_at__year=year)
        return render(request,'htmx/sales_report_table.html',{'delivered_products':delivered_products})


def monthly_salesreport(request):
    month=request.POST.get("month")
    if month=='0':
      delivered_products=order.objects.filter(status="delivered")  
      return render(request,'htmx/sales_report_table.html',{'delivered_products':delivered_products})
    else:
        delivered_products=order.objects.filter(status="delivered",created_at__month=month)
        return render(request,'htmx/sales_report_table.html',{'delivered_products':delivered_products})


def date_range_salesreport(request):
    from_date=request.POST.get("fromdate")
    print(from_date)
    to_date=request.POST.get("todate")
    print(to_date)

    if from_date == to_date:
        
        delivered_products = order.objects.filter(status="delivered",created_at__date=from_date)
        return render(request,'htmx/sales_report_table.html',{'delivered_products':delivered_products})
    else:

        delivered_products = order.objects.filter(status="delivered",created_at__range=[from_date, to_date])
        return render(request,'htmx/sales_report_table.html',{'delivered_products':delivered_products})


def export_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=sales_report'+ ".csv"
    writer=csv.writer(response)
    writer.writerow(['product id ','created date','tracking number','user','total price','payment mode'])
    delivered_products=order.objects.filter(status="delivered") 
    for products in delivered_products:
        writer.writerow([products.id,products.created_at,products.tracking_number,products.user.first_name,products.total_price,products.total_price])
    return response

def export_exl(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename=sales_report'+ ".xls"
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('sales-report')
    row_num=0
    font_style=xlwt.XFStyle()
    font_style.font.bold=True
    columns=['order id ','created date','tracking number','user','total price','payment mode']
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)
    font_style=xlwt.XFStyle()
    rows = order.objects.filter(status="delivered").values_list('id','created_at','tracking_number','user','total_price','payment_mode')

    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num,col_num, str(row[col_num]),font_style)

    wb.save(response)

    return response


# def export_pdf(request):
#     response=HttpResponse(content_type='application/pdf')
#     response['Content-Disposition']=' inline; attachment; filename=sales_report' + \
#      str(datetime.datetime.now())  +'.pdf'
#     response['Content-Transfer-Encoding']='binary'
#     html_string=render_to_string('sales-report-pdf.html',{"helooo":"my name stephin"})
#     html=HTML(string=html_string)
#     result=html.write_pdf()

 
#     with tempfile.NamedTemporaryFile(delete=True) as  output:
#         output.write(result)
#         output.flush()
#         output.seek(0)
#         #output=open(output.name,'rb')
#         response.write(output.read())
#     return response