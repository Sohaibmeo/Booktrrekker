from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register([Contact,ProductImage,Customer,Category,Product,Cart,CartProduct,Order])
@admin.register(Rating)
class ratingAdmin(admin.ModelAdmin):
    list_display=('user','movie','rating','rated_date')
