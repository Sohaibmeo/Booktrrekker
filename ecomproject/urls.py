
import imp
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static  

admin.site.site_header = "Login To Book Trekker Admin"
admin.site.site_title= "Book Trekker Dashboard"
admin.site.index_title  = "Welcome to the portal"
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("ecomapp.urls")),
]
# urlpatterns+=static()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
