# from asyncio.windows_events import NULL
# from django.utils.text import slugify 
from distutils.command.upload import upload
from email.mime import image




from django.db import models
from accounts.models import CustomUser
#  f
# Create your models here.


class user_address(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE) 
    fist_name=models.CharField(max_length=100,default="null")
    last_name=models.CharField(max_length=100,default="null")
    email=models.CharField(max_length=100,default="null")
    phone=models.CharField(max_length=15,default="null")
    addressline1=models.CharField(max_length=200,default="null")
    addressline2=models.CharField(max_length=200,default="null")
    city=models.CharField(max_length=100,default="null")
    state= models.CharField(max_length=100,default="null")
    country=models.CharField(max_length=100,default="null")
    zip_code=models.CharField(max_length=8,default="null")

    # def full_address(self):
    #     return f"{self.street}:{self.zipcode}:{self.city}"
    
    # def __str__(self):
    #     return self.full_address

class Category(models.Model):
    name=models.CharField(max_length=100)
    categoryIcon=models.ImageField(upload_to='img/catIcons',blank=True)
    offer=models.IntegerField(blank=True,null=True)
    offer_name=models.CharField(max_length=50,null=True,blank=True)
    is_offer=models.BooleanField(default=False)
    def __str__(self):
        return self.name

class subcategory(models.Model):
    name=models.CharField(max_length=100)
    subcategoryIcon=models.ImageField(upload_to='img/subcatIcons',blank=True)
    maincategory=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.name



class color(models.Model):
    name=models.CharField(max_length=100)
    colorIcon=models.ImageField(upload_to='img/colorIcons',blank=True)
    def __str__(self):
        return self.name


class size(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name




    


class brand(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to="img/product")
    
    def __str__(self):
        return self.name

class product(models.Model):
    product_name=models.CharField(max_length=100)
    product_title=models.CharField(max_length=100)
    Category=models.ForeignKey(Category,  on_delete=models.CASCADE) 
    subcategory=models.ForeignKey(subcategory,on_delete=models.CASCADE) 
    discription=models.TextField()
    color=models.ForeignKey(color,on_delete=models.CASCADE) 
    size=models.ForeignKey(size,on_delete=models.CASCADE) 
    brand=models.ForeignKey(brand,on_delete=models.CASCADE)
    is_new_item=models.BooleanField(blank=True,default=False)
    actual_price=models.IntegerField(null=True)
    discount_price=models.IntegerField(null=True)
    discount_rate=models.IntegerField(null=True)
    cover_image=models.ImageField(upload_to='productimages',blank=True)
    is_offer=models.BooleanField(default=True)
    stock=models.IntegerField(null=True)
    # slug=models.SlugField(unique=True,null=True)

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.product_name)
    #     super(product, self).save(*args, **kwargs)
   
    
    def __str__(self):
        return self.product_name
  
    def offercheck(self):
        if self.is_offer==True and self.Category.is_offer==True:
            if self.discount_rate>self.Category.offer:
                self.discount_price=self.discount_price *(self.discount_rate/100)
                self.save()
                return self.discount_rate
            else:
                self.discount_price=self.discount_price*(self.Category.offer/100)
                self.save()
                return self.Category.offer
        elif self.is_offer==False and self.Category.is_offer==True:
            return self.Category.offer
        elif self.is_offer==True and self.Category.is_offer==False:
            return self.discount_rate
        else:
            return self.discount_rate

            
class price(models.Model):
    productItem=models.ForeignKey(product, on_delete=models.CASCADE,null=True, related_name = "prices")
    actual_price=models.IntegerField(null=True)
    discount_price=models.IntegerField(null=True)
    discount_rate=models.IntegerField(null=True)   
    def __str__(self):
        return str(self.actual_price)

class media(models.Model):
   product=models.ForeignKey(product, on_delete=models.CASCADE)
   image1=models.ImageField(upload_to='productimages',blank=True)
   image2=models.ImageField(upload_to='productimages',blank=True)
   image3=models.ImageField(upload_to='productimages',blank=True)
   image4=models.ImageField(upload_to='productimages',blank=True)
   image5=models.ImageField(upload_to='productimages',blank=True)

class banners(models.Model):
   product=models.ManyToManyField(product,blank=True)
   discription=models.CharField(max_length=100)
   image=models.ImageField(upload_to='banners')
   banner_text=models.TextField(null=True)
   def __str__(self):
        return self.discription

class coupons(models.Model):
    couponcode=models.CharField(max_length=15)
    discription=models.CharField(max_length=200)
    discount_percentage=models.IntegerField(blank=True,null=True)
    user_is_used=models.ManyToManyField(CustomUser,blank=True)

    def __str__(self):
        return self.couponcode
  

class inventory(models.Model):
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    
    def __str__(self):
        return str(self.product)
