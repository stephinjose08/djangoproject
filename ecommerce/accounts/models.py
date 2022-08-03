import random
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, phone,email, password , **extra_fields):
        """Create and save a User with the given email and password."""
        if not phone:
            raise ValueError('The given phone must be set')

        email = self.normalize_email(email)
        user = self.model(phone=phone,email=email,password=password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone,email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone,email, password, **extra_fields)

    def create_superuser(self, phone,email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone,email, password, **extra_fields)

class CustomUser(AbstractUser):
    username=models.CharField(max_length=15,blank=True)
    phone=models.CharField(max_length=12,unique=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()


class code(models.Model):
    Otp=models.CharField(max_length=5)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)

    # def __str__(self):
    #     return str(self.Otp)
    
    # def save(self,*args,**kwargs):
    #     number=[x for x in range(10)]
    #     code_items=[]

    #     for i in range(5):
    #         num=random.choice(number)
    #         code_items.append(num)
        
    #     codestring="".join(str(item) for item in code_items)
    #     self.Otp=codestring
    #     return super().save(*args,**kwargs)

