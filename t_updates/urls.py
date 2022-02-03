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

    # Tech Updates
    path('tech-updates', views.updates, name="Tech Update Page"),

    # Offers & Promocode
    path('offers_promocode', views.offers_promocode,
         name="Offers & Promocode Page"),

    # About Page
    path('about', views.about, name="About Page"),

    # Shop Page
    path('shop', views.shop, name="Shop Page"),
    path('single_product/<int:id>', views.single_product,
         name="Single Product Page"),

    # My Account Page
    path('my_account', views.my_account, name="My Account Page"),
    path('my_account/make_changes', views.my_account, name="My Account Page"),
    path('make_changes', views.make_changes, name="Make Changes Page"),
    path('my_address', views.my_address, name="My Address Page"),

    path('wishlist', views.my_wishlist, name="My Wishlist Page"),
    path('add_wishlist', views.add_wishlist, name="Add Wishlist Page"),
    path('removeFromWishlist/<int:id>',
         views.removeFromWishlist, name="Remove Wishlist Item"),

    path('cart', views.cart, name="Cart Page"),
    path('add_cart', views.add_cart, name="Add Cart Page"),
    path('removeFromCart/<int:id>', views.removeFromCart, name="Add Cart Page"),

    # Blog
    path('blog', views.blog, name="Orders Page"),
    path("blogpost/<int:id>", views.blogpost, name="blogPost"),

    path('handle_signup', views.handle_signup, name="Sign Up Page"),
    path('handle_login', views.handle_login, name="Login Page"),
    path('handle_logout', views.handle_logout, name="Logout Page"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
