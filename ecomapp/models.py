from concurrent.futures.process import _MAX_WINDOWS_WORKERS
from distutils.command.upload import upload
import email
from email.policy import default
from importlib.machinery import FrozenImporter
from operator import truediv
from pyexpat import model
from tkinter import CASCADE
from typing import Tuple
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import User
from statistics import mode
from unicodedata import category
from django.db import models
from django.forms import CharField

# Create your models here.
# class Coupon(models.Model):
#     code=CharField(max_length=15)

#     def __str__(self):
#         return self.code






class Contact(models.Model):
    name = models.CharField(max_length=20,null=False,blank=False)
    email = models.CharField(max_length=30,null=False,blank=False)
    phone = models.CharField(max_length=13,null=False,blank=False)
    desc = models.CharField(max_length=500,null=False,blank=False)

    def __str__(self):
        return self.email





class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    full_name=models.CharField(max_length=200,null=False,blank=False)
    address= models.CharField(max_length=300,null=False,blank=False)
    joined_on=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.full_name

class Category(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(unique=True,blank=False,null=False),


    def __str__(self):
        return self.title


class Product(models.Model):
    title=models.CharField(max_length=200,null=False,blank=False)
    author=models.CharField(max_length=100,null=False,blank=False)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    slug=models.SlugField(unique=True,null=False,blank=False)
    image=models.ImageField(upload_to="products")
    marked_price=models.PositiveBigIntegerField(null=False,blank=False)
    selling_price=models.PositiveBigIntegerField(null=False,blank=False)
    description=models.TextField(null=False,blank=False)
    view_count=models.PositiveIntegerField(default=0)
    quantity=models.PositiveBigIntegerField(default=0)
    user=models.TextField(max_length=30,null=False,blank=False,default="Book Trekker")


    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="products/images/")

    def __str__(self):
        return self.product.title

# class ProductUpload(models.Model):
#     customer=models.CharField(max_length=100,blank=False,null=False)
#     # customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
#     # product=models.ForeignKey(Product,on_delete=models.CASCADE)



    def __str__(self):
        return "Product: " + str(self.id)


class Cart(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    total=models.PositiveBigIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart:"+str(self.id)

class CartProduct(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    rate=models.PositiveBigIntegerField(default=0)
    quantity=models.PositiveBigIntegerField(default=0)
    subtotal=models.PositiveBigIntegerField(default=0)


    def __str__(self):
        return "Cart:"+str(self.cart.id) + "CartProduct: " + str(self.id)


ORDER_STATUS= (
     ("Order Received","Order Received"),
     ("Order Processing","Order Processing"),
     ("On the way","On the way"),
     ("Completed","Completed"),
     ("Order Cancelled", "Order Cancelled"),
 )
class Order(models.Model):
     cart=models.OneToOneField(Cart, on_delete=models.CASCADE)
     ordered_by=models.CharField(max_length=200,null=False,blank=False)
     shipping_address=models.CharField(max_length=300,null=False,blank=False)
     mobile=models.CharField(max_length=13,null=False,blank=False)
     email=models.CharField(max_length=30,null=False,blank=False)
     subtotal=models.PositiveBigIntegerField(default=0)
     total=models.PositiveBigIntegerField(default=0)
     order_status=models.CharField(max_length=200,choices=ORDER_STATUS)
     created_at=models.DateTimeField(auto_now_add=True)



     def __str__(self):
        return "Order: " + str(self.id)

class Rating(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    movie=models.ForeignKey(Product,on_delete=models.CASCADE,default=None)
    rating=models.CharField(max_length=70)
    rated_date=models.DateTimeField(auto_now_add=True)


