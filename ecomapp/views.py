from django.core.validators import validate_email 
from django.core.exceptions import ValidationError
from genericpath import exists
from itertools import product
from socket import fromshare
from django.core.paginator import Paginator
from django import forms
from math import prod
from django.contrib import messages
from pipes import Template
from re import template
from sre_constants import SUCCESS

from urllib import request
from wsgiref.util import request_uri
from django.shortcuts import render,redirect    
from django.views.generic import View,TemplateView,CreateView,FormView  ,DetailView , ListView
from .models import *
from .forms import CheckoutForm , CustomerRegistrationForm,CustomerLoginForm,ProductForm,PasswordForgotForm,PasswordResetForm
from django.urls import reverse_lazy , reverse
# for complex searching of products import Q
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from .utils import password_reset_token

from django.core.mail import send_mail
from django.conf import settings


# libraries for recommendations system

import numpy as np
import pandas as pd



# Create your views here.
# if the user is logged in the it is to be related with the cart
class EcomMixin(object):
    def dispatch(self,request,*args,**kwargs):
        # check if cart exists or not
        cart_id=request.session.get("cart_id")
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
            # to assign customer to a cart
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer=request.user.customer
                cart_obj.save()

        return super().dispatch(request,*args,**kwargs)

class HomeView(EcomMixin,TemplateView):
    template_name="home.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        all_products=Product.objects.all().order_by("-id")
        # how many number of items to be shown on the home page 
        paginator=Paginator(all_products,4)
        page_number=self.request.GET.get('page')
        product_list=paginator.get_page(page_number)
        context['product_list']=product_list
        return context

class AllProductsView(EcomMixin, TemplateView):
    template_name="allproducts.html"

    def get_context_data(self, **kwargs):
          context=super().get_context_data(**kwargs)
          context["allcategories"]=Category.objects.all()

          return context

class ProductDetailView(EcomMixin,TemplateView):
    template_name="productdetail.html"
    def get_context_data(self, **kwargs):
          context=super().get_context_data(**kwargs)
          url_slug=self.kwargs['slug']
          product=Product.objects.get(slug=url_slug)
          product.view_count+=1
          product.save()    
          context['product']=product
          return context      
class AddToCartView(EcomMixin,TemplateView):
    template_name = "addtocart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get product id from requested url
        product_id = self.kwargs['pro_id']

        # get product
        product_obj = Product.objects.get(id=product_id)

       
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)

            # item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
#  ---------------------------------------------
                # product_obj.quantity-=1
                # product_obj.save()
                # ----------------------------------------------------------
            # new item is added in cart
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
               
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()

        return context

class ManageCartView(EcomMixin,TemplateView):
    def get(self,request,*args,**kwargs):
        # print("this is manage cart view")
        cp_id=self.kwargs["cp_id"]
        action=request.GET.get("action")
        cp_obj=CartProduct.objects.get(id=cp_id)
        

        product=Product.objects.get(cartproduct__id=cp_id)
        # print(product.quantity)


        #  to deduct the stock of product everytime add to cart 
        
        cart_obj=cp_obj.cart
        # product=Product.objects.get(id=cp_id)

        original_quantity=0
        print("Product Quantity",product.quantity)
        
        
        if action=="inc":
            if cp_obj.quantity == product.quantity:
                messages.warning(request, 'This book is now out of stock!!!')
                return redirect ("ecomapp:mycart")

            else:
                cp_obj.quantity+=1
                cp_obj.subtotal+=cp_obj.rate
                cp_obj.save()
                cart_obj.total+=cp_obj.rate
                cart_obj.save()
                print("Cart Product Quantity",cp_obj.quantity)
                original_quantity=product.quantity-cp_obj.quantity
                print("Original Quantity",original_quantity)
     
            
        elif action=="dcr":
            if cp_obj.quantity<=0 or original_quantity== product.quantity:
                messages.warning(request, 'Can^t do that more!!!')
                return redirect ("ecomapp:mycart")
            else:
                cp_obj.quantity-=1
                cp_obj.subtotal-=cp_obj.rate
                cp_obj.save()
                cart_obj.total-=cp_obj.rate
                cart_obj.save()
                original_quantity=product.quantity-cp_obj.quantity
                print("Cart Product Quantity",cp_obj.quantity)
                print("Original Quantity",original_quantity)
   
        elif action=="rmv":
            cart_obj.total-=cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        
        return redirect("ecomapp:mycart")
    # template_name="managecart.html" 

class EmptyCartView(EcomMixin,TemplateView):
    def get(self,request,*args,**kwargs):
        cart_id=request.session.get("cart_id",None)
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
            cart_obj.cartproduct_set.all().delete()
            cart_obj.total=0
            cart_obj.save()
        return redirect("ecomapp:mycart")
         
class CheckoutView(EcomMixin,CreateView):
    template_name="checkout.html"
    form_class=CheckoutForm
    success_url=reverse_lazy("ecomapp:home")
# this function checks the condition tht if the user is already logged in before checkout or not
    def dispatch(self, request, *args, **kwargs):
        user =request.user
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            # to append url patteren  after login he/she should directly return to checkout
            return redirect("/login/?next=/checkout/")
        # print(user)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id=self.request.session.get("cart_id",None )
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
        else:
            cart_obj=None
        context['cart']=cart_obj
        return context
    def form_valid(self,form):
        cart_id=self.request.session.get('cart_id')
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
            form.instance.cart=cart_obj
            print("Checkout",cart_obj)
            form.instance.subtotal=cart_obj.total
            form.instance.total=cart_obj.total  
            form.instance.order_status="Order Received"
           

            for cp in cart_obj.cartproduct_set.all():
                cp.product.quantity=cp.product.quantity-cp.quantity
                cp.product.save()
                print(cp.product.quantity)



            del self.request.session['cart_id']
        else:
            return redirect("ecomapp:home")    
        return super().form_valid(form)    

class MyCartView(EcomMixin,TemplateView): 
  template_name="mycart.html"

  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id=self.request.session.get("cart_id", None)
        if cart_id:
          cart=Cart.objects.get(id=cart_id)
        else:
          cart=None  
        context['cart']=cart
        return context

class CustomerRegistrationView(CreateView):
    template_name="customerregistration.html"
    form_class=CustomerRegistrationForm
    success_url=reverse_lazy("ecomapp:home")
    
    def form_valid(self,form):
        username=form.cleaned_data.get("username")

        email=form.cleaned_data.get("email")

        password=form.cleaned_data.get("password")

        user=User.objects.create_user(username,email,password)
        form.instance.user=user
        
        login(self.request,user)
        request.session ['user_id']=user.id
        request.session ['user_email']=user.email
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url=self.request.GET.get("next")
            return next_url
        else:
            return self.success_url



class CustomerLogoutView(TemplateView):
    def get(self,request):
        # request parameter to logout from user     
        logout(request)
        return redirect("ecomapp:home")


class CustomerLoginView(FormView):
    template_name="customerlogin.html"
    form_class=CustomerLoginForm
    success_url=reverse_lazy("ecomapp:home")
    # it is post method and is available in formView,createView etc
    def form_valid(self,form):
        uname=form.cleaned_data.get("username")
        pword=form.cleaned_data.get("password")
        usr =authenticate(username=uname,password=pword)
        if usr is not None and Customer.objects.filter(user=usr):
            login(self.request,usr)
        else:
            # you can also use self.template_name in place of customerlogin.html
            return render(self.request,"customerlogin.html",{"form":CustomerLoginForm,"error":"Invalid Credentials"
            })
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url=self.request.GET.get("next")
            return next_url
        else:
            return self.success_url
         

class AboutView(EcomMixin,TemplateView):
    template_name="about.html" 

class ContactView(EcomMixin,TemplateView):
    template_name="contact.html"

    def post(self,request,*args,**kwargs):
        name=request.POST.get('name',default="" )
        email=request.POST.get('email',default="")
        phone=request.POST.get('phone',default="" )
        desc=request.POST.get('desc',default="" ) 
        query=Contact(name=name,email=email,phone=phone,desc=desc)
        query.save()
        
        return redirect("/all-products/")




class CustomerProfileView(TemplateView):
    template_name="customerprofile.html" 
    def dispatch(self, request, *args, **kwargs):
        usr =request.user
        if request.user.is_authenticated and Customer.objects.filter(user=usr):
            pass
        else:
            # to append url patteren  after login he/she should directly return to checkout
            return redirect("/login/?next=/profile/")
        # print(user)
        return super().dispatch(request, *args, **kwargs)

        
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)  
        customer=self.request.user.customer
        context['customer']=customer   
        # need to fileter out orders whose cart customers = customer above
        orders=Order.objects.filter(cart__customer=customer).order_by("-id") 
        context['orders']=orders
        # get the products uploaded by particular user
        uploadedProducts=ProductUpload.objects.filter(customer=customer)
        context['uploadedProducts']=uploadedProducts
        return context

    
class CustomerOrderDetailView(DetailView):
    template_name="customerorderdetail.html"
    def dispatch(self, request, *args, **kwargs):
        usr =request.user
        if request.user.is_authenticated and Customer.objects.filter(user=usr): 
            order_id=self.kwargs['pk']
            order=Order.objects.get(id=order_id)
            if request.user.customer!=order.cart.customer:
                return redirect("ecomapp:customerprofile")
        else:
            # to append url patteren  after login he/she should directly return to checkout
            return redirect("/login/?next=/profile/")
        # print(user)
        return super().dispatch(request, *args, **kwargs)
    model=Order
    # through this u can send customer name and we can get order object with following name
    context_object_name="ord_obj"



class PasswordForgotView(FormView):
    template_name="forgotpassword.html"
    form_class=PasswordForgotForm
    success_url="/forgot-password/?m=s"

    def form_valid(self,form):
        email=form.cleaned_data.get("email")
        # get current host ip/domain     
        url = self.request.META['HTTP_HOST']
        # get customer and then user
        customer = Customer.objects.get(user__email=email)
        user = customer.user
        # send mail to the user with email
        text_content = 'Please Click the link below to reset your password. '
        html_content = url + "/password-reset/" + email + \
        "/" + password_reset_token.make_token(user) + "/"
        send_mail(
            'Password Reset Link | Django Book trekker',
            text_content + html_content,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )


        return super().form_valid(form)


class PasswordResetView(FormView):
    template_name = "passwordreset.html"
    form_class = PasswordResetForm
    success_url = "/login/"

    def dispatch(self, request, *args, **kwargs):
        # below email and token got from url path (kwargs)
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        token = self.kwargs.get("token")
        if user is not None and password_reset_token.check_token(user, token):
            pass
        else:
            return redirect(reverse("ecomapp:passworforgot") + "?m=e")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password = form.cleaned_data['new_password']
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return super().form_valid(form)



class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        usr =request.user
        if request.user.is_authenticated and Customer.objects.filter(user=usr):
            pass
        else:
            # to append url patteren  after login he/she should directly return to checkout
            return redirect("/login/?next=/customer-product/add/")
        # print(user)
        return super().dispatch(request, *args, **kwargs)        





class SearchView(TemplateView):
    template_name="search.html"

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        kw=self.request.GET.get('keyword')
        #  here iconyains meanes there is no case sensitivity in searchong products
        results=Product.objects.filter(Q(title__icontains=kw) | Q(description__icontains=kw) 
        | Q(return_policy__icontains=kw))
        context['results']=results
        return context


# search by book name
class SearchBookNameView(TemplateView):
    template_name="searchbookname.html"

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        bookname=self.request.GET.get('bookname')
        #  here icontains meanes there is no case sensitivity in searching products
        results=Product.objects.filter(Q(title__icontains=bookname))
        context['results']=results
        return context


# search by category

class SearchCategoryView(TemplateView):
    template_name="searchcategory.html"

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        bookcategory=self.request.GET.get('bookcategory')
        #  here icontains meanes there is no case sensitivity in searchong products
        results=Product.objects.filter(Q(title__icontains=bookcategory) | Q(description__icontains=bookcategory) 
        | Q(return_policy__icontains=bookcategory))
        context['results']=results
        return context

# search by author

class SearchAuthorView(TemplateView):
    template_name="searchauthor.html"

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        searchauthor=self.request.GET.get('bookauthor')
        #  here icontains meanes there is no case sensitivity in searchong products
        results=Product.objects.filter(Q(author__icontains=searchauthor))
        context['results']=results
        return context


# customer product upload 

class CustomerProductCreateView(LoginRequiredMixin,CreateView):
    template_name="customerproductcreate.html"
    form_class=ProductForm
    success_url=reverse_lazy("ecomapp:allproducts")

    def form_valid(self, form):
        p=form.save()
        images=self.request.FILES.getlist("more_images")
        for i in images:
            ProductImage.objects.create(product=p,image=i)
# track history of user uploaded products
        usr =self.request.user
        ProductUpload.objects.create(customer=usr,product=p)
        

        # userProduct=ProductUpload.objects.filtesr()
        # =ProductUpload()
        print(usr)

        return super().form_valid(form)
       


# customer product upload ends here 



# Feedback protion
def Review_rate(request,id):
    if request.method=="GET":
        prod_id=request.GET.get('prod_id')
        product=Product.objects.get(id=prod_id)
        comment=request.GET.get("comment")
        rate=request.GET.get("rate")
        user=request.user
        Review(user=user,product=product,comment=comment,rate=rate).save()
        return redirect("productdetail.html",id=prod_id)




