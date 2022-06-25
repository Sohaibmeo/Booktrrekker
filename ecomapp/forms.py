from django import forms 
from django.core.validators import RegexValidator
from .models import Order,Customer,Product
from django.contrib.auth.models  import User 
from django.core.validators import validate_email 
from django.core.exceptions import ValidationError
import re
class CheckoutForm(forms.ModelForm):
    ordered_by=forms.CharField(widget=forms.TextInput(attrs={
        "class":"form-control",
        "multiple":True}))
    shipping_address=forms.CharField(widget=forms.TextInput(attrs={
        "class":"form-control",
        "multiple":True}))
    mobile=forms.IntegerField(widget=forms.TextInput(attrs={
        "class":"form-control",
        "multiple":True}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        "class":"form-control",
        "multiple":True}))

    class Meta:
        model=Order
        fields=["ordered_by","shipping_address","mobile","email"]


class CustomerRegistrationForm(forms.ModelForm):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    username=forms.CharField(widget=forms.TextInput(attrs={
        "class":"form-control",
        'pattern':'[[0-9a-zA-Z]+',
        "multiple":True}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        "class":"form-control",
        'pattern':'[[0-9a-zA-Z]+',
        "multiple":True}))
    email=forms.CharField(widget=forms.EmailInput(attrs={
        "class":"form-control",
        "multiple":True}))

    address=forms.CharField(widget=forms.TextInput(attrs={
        "class":"form-control",
        "multiple":True}))
    full_name=forms.CharField(widget=forms.TextInput(attrs={
        "class":"form-control",
        "multiple":True}))
    class Meta:
        model=Customer
        fields=["username","password","email", "full_name","address"]
    # for username validation
    def clean_username(self):
        uname=self.cleaned_data.get("username")
        if len(uname)>7 & uname.isalnum() and not User.objects.filter(username=uname):
            return uname
        else:
            if len(uname)<7:
                raise forms.ValidationError("Username length must be gretaer than 7")
            elif not uname.isalnum():
                raise forms.ValidationError("Username length must be alphanumeric")
            elif User.objects.filter(username=uname):
                raise forms.ValidationError("User already exists")
            else:
                raise forms.ValidationError("Information is not properly given") 
           

        # if not uname.isalnum():
        #     raise forms.ValidationError("Username must contains alphabets and numbers")
        # if User.objects.filter(username=uname):
        #     raise forms.ValidationError("User with that userame already exists")
        # return uname    


        # validation for email
    
    def clean_email(self):
        email=self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email Already Exists")
        return email 

# validation for password

    def clean_password(self):
        pas=self.cleaned_data.get("password")
        if len(pas)<8:
            raise forms.ValidationError("Password length too short")
        
        if not pas.isalnum():
            raise forms.ValidationError("Password must contains alphabets and numbers")
        # if pas==username:
        #     raise forms.ValidationError("Username and password must not be same")

        return pas

      

class CustomerLoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={
        "class":"form-control",
        "multiple":True}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        "class":"form-control",
        "multiple":True}))

# admin forms
class ProductForm(forms.ModelForm):
    more_images=forms.FileField(required=False,widget=forms.FileInput(attrs={
        "class":"form-control",
        "multiple":True
    }))
    class Meta:
        model=Product
        fields=['title','author','slug','category','image','marked_price','selling_price','description',
        'quantity']

        widgets={
             "title":forms.TextInput(attrs={
                 "class":"form-control",
                 "placeholder":"Enter book name here!!!"
           }),
           "author":forms.TextInput(attrs={
                 "class":"form-control",
                 "placeholder":"Author Name"
           }),
           "slug":forms.TextInput(attrs={
                 "class":"form-control",
                 "placeholder":"Enter unique slug here!!!"
           }),
           "category":forms.Select(attrs={
                "class":"form-control"
           }),
           "image":forms.ClearableFileInput(attrs={
                "class":"form-control"
           }),
           "marked_price":forms.NumberInput(attrs={
                "class":"form-control",
                "placeholder":"Marked Price of the book"
           }),
           "selling_price":forms.NumberInput(attrs={
                "class":"form-control",
                "placeholder":"Selling Price of the book"
           }),
           "description":forms.Textarea(attrs={
              
                "class":"form-control",
                "placeholder":"Description of the book !!"
                
           }),
           "quantity":forms.NumberInput(attrs={
                "class":"form-control",
                "placeholder":"How much stock?"
           }),
        }

class PasswordForgotForm(forms.Form):
    email=forms.CharField(widget=forms.EmailInput(attrs={
        "class":"form-control",
        "placeholder":"Enter your email used in account"
    }))
    # if u want to validate field only eg: email
    def clean_email(self):
        e=self.cleaned_data.get("email")
        if Customer.objects.filter(user__email=e).exists():
            pass
        else:
            raise forms.ValidationError("Customer with this account does not exist")
        return e

class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
        'placeholder': 'Enter New Password',
    }), label="New Password")
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
        'placeholder': 'Confirm New Password',
    }), label="Confirm New Password")

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_new_password = self.cleaned_data.get("confirm_new_password")
        if new_password != confirm_new_password:
            raise forms.ValidationError(
                "New Passwords did not match!")
        return confirm_new_password
