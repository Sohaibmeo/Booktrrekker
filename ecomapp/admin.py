from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register([Contact,ProductImage,Customer,Category,Product,Cart,CartProduct,Order,ProductUpload ,Review]) 
