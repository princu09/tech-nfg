from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.views.generic import RedirectView

urlpatterns = [

    # Basic Page For Everyone
    url(r'^$', RedirectView.as_view(url='home')),
    path('home', views.index, name="Main Page"),

    # Shop Page
    path('shop', views.shop, name="Shop Page"),
    path('single_product/<int:id>', views.single_product,
         name="Single Product Page"),
    path('product_category/<str:category>', views.product_category,
         name="Product Category Page"),

    # Compare Product
    path('compare_product/<int:prod1>/<int:prod2>', views.compare_product,
         name="Compare Product Page"),

    # Offers & Promocode
    path('offers_promocode', views.offers_promocode,
         name="Offers & Promocode Page"),


    # Tech Updates
    path('tech-updates', views.updates, name="Tech Update Page"),


    # About Page
    path('about', views.about, name="About Page"),


    # My Account Page
    path('my_account', views.my_account, name="My Account Page"),
    path('my_account/make_changes', views.my_account, name="My Account Page"),
    path('make_changes', views.make_changes, name="Make Changes Page"),
    path('account_setting', auth_views.PasswordChangeView.as_view(
        template_name='include/account_setting.html',
        success_url='/'
    ), name="Account Setting Page"),
    path('my_orders', views.my_orders, name="My Orders Page"),
    path('view_bill/<int:id>', views.view_bill, name="View Bill"),


    # Wishlist Page
    path('wishlist', views.my_wishlist, name="My Wishlist Page"),
    path('add_wishlist', views.add_wishlist, name="Add Wishlist Page"),
    path('removeFromWishlist/<int:id>',
         views.removeFromWishlist, name="Remove Wishlist Item"),


    # Cart Page
    path('cart', views.cart, name="Cart Page"),
    path('add_cart', views.add_cart, name="Add Cart Page"),
    path('removeFromCart/<int:id>', views.removeFromCart, name="Add Cart Page"),
    path('check_cart_price', views.check_cart_price, name="Cart Price Checking"),
    path('checkout', views.checkout, name="Checkout Checking"),


    # Blog
    path('blog', views.blog, name="Orders Page"),
    path("blogpost/<int:id>", views.blogpost, name="blogPost"),


    # Login Signup
    path('handle_signup', views.handle_signup, name="Sign Up Page"),
    path('handle_login', views.handle_login, name="Login Page"),
    path('handle_logout', views.handle_logout, name="Logout Page"),


    # Subscribe & Search
    path('subscribe', views.subscribe, name="Subscribe Page"),
    path('search', views.search, name="Search Page"),

    # Place Order
    path('place_order', views.place_order, name="Place Order Page"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
