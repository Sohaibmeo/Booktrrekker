from xmlrpc.client import APPLICATION_ERROR
from django.urls import path
from .views import*
from . import views

app_name="ecomapp"
urlpatterns=[
    path("", HomeView.as_view(),name="home"),
    path("about/", AboutView.as_view(),name="about"),
    path("contact-us/", ContactView.as_view(),name="contact"),
    path("all-products/", AllProductsView.as_view(),name="allproducts"),
    path("product/<slug:slug>/", ProductDetailView.as_view(),name="productdetail"),
    path("add-to-cart-<int:pro_id>/",AddToCartView.as_view(),name="addtocart"),
    path("my-cart/",MyCartView.as_view(),name="mycart"),
    path("manage-cart/<int:cp_id>/",ManageCartView.as_view(),name="managecart"),
    path("empty-cart/",EmptyCartView.as_view(),name="emptycart"),
    path("remove-product/<int:prod_id>",RemoveProductView.as_view(),name="removeproduct"),
    path("checkout/",CheckoutView.as_view(),name="checkout"),
    path("register/",CustomerRegistrationView.as_view(),name="customerregistration"),
    path("logout/",CustomerLogoutView.as_view(),name="customerlogout"),
    path("login/",CustomerLoginView.as_view(),name="customerlogin"),
    path("profile/",CustomerProfileView.as_view(),name="customerprofile"),


    path("profile/order-<int:pk>/",CustomerOrderDetailView.as_view(),name="customerorderdetail"),
    path("mydashboard/",MyDashboardView.as_view(),name="orderedbooks"),
    path('create-checkout-session/', views.create_checkout_session), # new
    path('config/', views.stripe_config),
    path("search/",SearchView.as_view(),name="search"),
    path("searchauthor/",SearchAuthorView.as_view(),name="searchauthor"),
    path("searchbookname/",SearchBookNameView.as_view(),name="searchbookname"),
    path("searchcategory/",SearchCategoryView.as_view(),name="searchcategory"),

    # path("want-to-sell/",WantToSellView.as_view(),name="wanttosell"),
    # path("review/", views.Review_rate, name="review"),
    path("forgot-password/", PasswordForgotView.as_view(), name="passwordforgot"),
    path("password-reset/<email>/<token>/",PasswordResetView.as_view(),name="passwordreset"),
    path('dashboard/',views.dashboard,name="dashboard"),
    # customer  product upload starts here
    path("customer-product/add/", CustomerProductCreateView.as_view(),name="customerproductcreate"),

]
