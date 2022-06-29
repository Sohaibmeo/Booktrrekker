from cProfile import label
from django import forms
from .models import *
from django.core.validators import RegexValidator
from .models import Order,Customer,Product
from django.contrib.auth.models  import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
class CheckoutForm(forms.ModelForm):
    ordered_by=forms.CharField(widget=forms.TextInput(attrs={
        # "class":"form-control",
        'size': '20',
        'style': 'font-size: medium',
        'style':'width :40px',
        'style':  'height: 30px',
        
        }))
    shipping_address=forms.CharField(widget=forms.TextInput(attrs={
        # "class":"form-control",
        'size': '20',
        'style': 'font-size: medium',
        'style':'width :40px',
        'style':  'height: 30px',
        
        }))
    mobile=forms.IntegerField(widget=forms.TextInput(attrs={
        # "class":"form-control",
         'size': '20',
        'style': 'font-size: medium',
        'style':'width :40px',
        'style':  'height: 30px',
        
        }))
    mobile = forms.CharField(max_length=11,min_length=11 ,validators=[RegexValidator(
        r'^(\+92|03|92)[0-9]{9}$', message="Enter a valid mobile#")])
     
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        # "class":"form-control",
         'size': '20',
        'style': 'font-size: medium',
        'style':'width :40px',
        'style':  'height: 30px',
        
        }))
    email= forms.CharField(max_length=30, validators=[RegexValidator(
        r'^[a-z0-9]+[0-9]+@gmail.com+$', message="Enter a valid gmail id")])
    class Meta:
        model=Order
        fields=["ordered_by","shipping_address","mobile","email"]


class CheckoutForm(forms.ModelForm):
    ordered_by=forms.CharField(widget=forms.TextInput(attrs={
        # "class":"form-control",
        'size': '20',
        'style': 'font-size: medium',
        'style':'width :40px',
        'style':  'height: 30px',
        
        }))    
    shipping_address=forms.CharField(widget=forms.TextInput(attrs={
        # "class":"form-control",
        'size': '20',
        'style': 'font-size: medium',
        'style':'width :40px',
        'style':  'height: 30px',
        
        }))
    mobile=forms.IntegerField(widget=forms.TextInput(attrs={
        # "class":"form-control",
         'size': '20',
        'style': 'font-size: medium',
        'style':'width :40px',
        'style':  'height: 30px',
        
        }))
    mobile = forms.CharField(max_length=11,min_length=11 ,validators=[RegexValidator(
        r'^(\+92|03|92)+[0-9]{9}$', message="Enter a valid mobile#")])
     
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        # "class":"form-control",
         'size': '20',
        'style': 'font-size: medium',
        'style':'width :40px',
        'style':  'height: 30px',
        "multiple":True
        }))
    email= forms.CharField(max_length=30, validators=[RegexValidator(
        r'^[a-z0-9]+[0-9]+@gmail.com+$', message="Enter a valid gmail id")])
    class Meta:
        model=Order
        fields=["ordered_by","shipping_address","mobile","email"]


class CustomerRegistrationForm(forms.ModelForm):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    username=forms.CharField(widget=forms.TextInput(attrs={
        'autofocus': 'autofocus',

        'size': '20',
        'style': 'font-size: medium',
        'style':'width :40px',
        'style':  'height: 30px'
        # "class":"form-control",
        # 'pattern':'[[0-9a-zA-Z]+',
        # "multiple":True
        }))
    username = forms.CharField(max_length=20, validators=[RegexValidator(
        r'^(?=.{8,20}$)(?:[a-zA-Z\d]+(?:(?:\.|-|_)[a-zA-Z\d])*)+[a-zA-Z0-9]+[0-9]+$', message="Enter a valid username")])
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        # "class":"form-control",
        # 'pattern':'[[0-9a-zA-Z]+',
        # "multiple":True
        'label':"One Capital Letter,Special Character,One Number,Length Should be 8-18",
        'autofocus': 'autofocus',
        'autocomplete': 'off',
        'style':'width :40px',
        'style':  'height: 30px',
        'size': '20',
        'style': 'font-size: medium'
        }))

    password= forms.CharField(min_length=8, validators=[RegexValidator(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$', message="Password must contain 1:Capital Letter,Special Character,1:Number & Length Should be 8-18")])
    email=forms.CharField(widget=forms.EmailInput(attrs={
        # "class":"form-control",
        # "multiple":True,
        'autofocus': 'autofocus',
        'autocomplete': 'off',
        'size': '20',
        'style':'width :40px',
        'style':  'height: 30px',
        'style': 'font-size: medium'
        }))

    email= forms.CharField(max_length=30, validators=[RegexValidator(
        r'^[a-z0-9]+[0-9]+@gmail.com+$', message="Enter a valid gmail id")])

    address=forms.CharField(widget=forms.TextInput(attrs={
        # "class":"form-control",
        # "multiple":True
        'autofocus': 'autofocus',
        'autocomplete': 'off',
        'size': '20',
        'style':'width :40px',
        'style':  'height: 30px',
        'style': 'font-size: medium'
         }))
    full_name=forms.CharField(widget=forms.TextInput(attrs={
        # "class":"form-control",
        # "multiple":True
        'autofocus': 'autofocus',
        'autocomplete': 'off',
        'size': '20',
        'style': 'font-size: medium',
        }))
    class Meta:
        model=Customer
        fields=["username","password","email", "full_name","address"]
    # for username validation
    def clean_username(self):
        uname=self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError("User already exists")

        return uname

        # else:
        #     if len(uname)<7:
        #         raise forms.ValidationError("Username length must be gretaer than 7")
        #     elif not uname.isalnum():
        #         raise forms.ValidationError("Username length must be alphanumeric")
        #     elif User.objects.filter(username=uname):
        #         raise forms.ValidationError("User already exists")
        #     else:
        #         raise forms.ValidationError("Information is not properly given")


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


        return pas



class CustomerLoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={
        # "class":"form-control",
        # "multiple":True
        'autofocus': 'autofocus',
        'autocomplete': 'off',
        'size': '20',
        'style': 'font-size: medium',
        }))
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        # "class":"form-control",
        # "multiple":True
        'autofocus': 'autofocus',
        'autocomplete': 'off',
        'size': '20',
        'style': 'font-size: medium',
        }))

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
                    # 'autofocus': 'autofocus',
                    # 'autocomplete': 'off',
                    #  'size': '20',
                    #  'style': 'font-size: large',
                    # "placeholder":"Enter book name here!!!"
           }),
           "author":forms.TextInput(attrs={
                 "class":"form-control",
                    # 'autofocus': 'autofocus',
                    # 'autocomplete': 'off',
                    #  'size': '20',
                    #  'style': 'font-size: large',
                    # "placeholder":"Author Name!!!"
                 
           }),  
           "slug":forms.TextInput(attrs={
                 "class":"form-control",
                # 'autofocus': 'autofocus',
                #     'autocomplete': 'off',
                #      'size': '20',
                #      'style': 'font-size: large',
                #  "placeholder":"Enter unique slug here!!!"
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
        # "class":"form-control",
        'autofocus': 'autofocus',
        'autocomplete': 'off',
        'size': '20',
        'style': 'font-size: large',
        "placeholder":"Your email!!"
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
    new_password=forms.CharField(widget=forms.PasswordInput(attrs={
        # "class":"form-control",
        # 'pattern':'[[0-9a-zA-Z]+',
        # "multiple":True
        'autofocus': 'autofocus',
        'autocomplete': 'off',
        'style':'width :40px',
        'style':  'height: 30px',
        'size': '20',
        'style': 'font-size: medium'
        }))

    new_password= forms.CharField(min_length=8, validators=[RegexValidator(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$', message="Password must contain 1:Capital Letter,Special Character,1:Number & Length Should be 8-18")])
    # confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
    #     'class': 'form-control',
    #     'autocomplete': 'new-password',
    #     'placeholder': 'Confirm New Password',
    # }), label="Confirm New Password")
    confirm_new_password=forms.CharField(widget=forms.PasswordInput(attrs={
        # "class":"form-control",
        # 'pattern':'[[0-9a-zA-Z]+',
        # "multiple":True

        'autofocus': 'autofocus',
        'autocomplete': 'off',
        'style':'width :40px',
        'style':  'height: 30px',
        'size': '20',
        'style': 'font-size: medium'
        }))

    confirm_new_password= forms.CharField(min_length=8, validators=[RegexValidator(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$', message="Password must contain 1:Capital Letter,Special Character,1:Number & Length Should be 8-18")])
    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_new_password = self.cleaned_data.get("confirm_new_password")
        if new_password != confirm_new_password:
            raise forms.ValidationError(
                "New Passwords did not match!")
        return confirm_new_password


class AddRatingForm(forms.ModelForm):
    class Meta:
        model=Rating
        fields=['rating']
        labels={'rating':'Rating'}
        widgets={
            'rating':forms.TextInput(attrs={'type':'range','step':'1','min':'0','max':'5','class':{'custom-range','border-0'}})
        }
