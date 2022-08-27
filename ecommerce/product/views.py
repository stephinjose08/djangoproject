
from unicodedata import category, name
from django.http import HttpResponse
from django.shortcuts import render

from .models import product,Category,media,banners,price,brand, size

# Create your views here.
def grid_view(request,bid=0):
  
     # products=product.objects.filter(banners.objects.get(bid))
     # print(products)
     if bid==0:
          products=product.objects.all()
          count=products.count()
          return  render(request,'shop-grid-box.html',{'products':products,'count':count})
     else:

          banner=banners.objects.get(id=bid)
          products=banner.product.all()
          count=products.count()
          #products=banners.objects.filter(product_)
          items_price=price.objects.filter(productItem_id__in=products.all())
          image=media.objects.filter(product_id__in=products.all())
          print(products)
          ziped_data=zip(products,list(image))
          return  render(request,'shop-grid-box.html',{'products':products,'count':count})

def detail_view(request,id):

     product_detail=product.objects.get(id=id)
     # item_price=price.objects.get(productItem_id=id)
     image=media.objects.get(product_id=id)
     # ziped_data=zip(product_detail,item_price,list(image))
     related=product.objects.filter(Category=2)
     print(product.objects.filter(Category=2).count())

     return  render(request,'product-details.html',{'product_detail':product_detail,'image':image,'related':related})


def brandwise(request,brandname):
    products=product.objects.filter(brand_id=brand.objects.get(name=brandname))
#     items_price=price.objects.filter(productItem_id__in=products.all())
#     image=media.objects.filter(product_id__in=products.all())
    count=products.count()
#     ziped_data=zip(products,items_price,list(image))
    return  render(request,'shop-grid-box.html',{'products':products,'count':count})

def categorywise(request,id):
    products=product.objects.filter(Category=id)
#     items_price=price.objects.filter(productItem_id__in=products.all())
#     image=media.objects.filter(product_id__in=products.all())
    count=products.count()
#     ziped_data=zip(products,items_price,list(image))
    return  render(request,'shop-grid-box.html',{'products':products,'count':count})


def searchgrid(request,bid):
     name=request.POST.get('search')
     print(name)
     items=product.objects.filter(product_title__icontains=name)
     # print(items.product_title)
     return render(request,'htmx/search_gird.html',{"products":items})
# def size_sort(request,size):
#      products=product.objects.all()
#      return render(request,'htmx/search_gird.html',{"products":products})
