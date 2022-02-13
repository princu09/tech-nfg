from email.utils import format_datetime
from statistics import mode
from unicodedata import category
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
import jsonfield


class Address(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()

    def __str__(self):
        return f"Id : {self.id}"


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    badge = models.CharField(max_length=30)
    title = models.CharField(max_length=250)
    desc = models.TextField()
    shortDesc = models.CharField(max_length=200)
    price = models.IntegerField()
    category = models.TextField()
    sku = models.CharField(max_length=50)
    rating = models.IntegerField()
    images1 = models.ImageField(upload_to='media')
    images2 = models.ImageField(upload_to='media')
    images3 = models.ImageField(upload_to='media')
    images4 = models.ImageField(upload_to='media')
    images5 = models.ImageField(upload_to='media')

    def __str__(self):
        return f"Id : {self.id}" " | " f"Title : {self.title}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    itemLen = models.IntegerField(primary_key=False)


class Blogpost(models.Model):
    post_id = models.AutoField(primary_key=True)
    batch_title = models.CharField(max_length=50, default="NorthFoxGroup")
    title = models.CharField(max_length=150)
    pub_date = models.DateField()
    main_content = models.CharField(max_length=50000, default="")
    heading = models.CharField(max_length=500, default="")
    content_heading = models.CharField(max_length=500, default="")
    sub_heading = models.CharField(max_length=500, default="")
    sub_content_heading = models.CharField(max_length=500, default="")
    thumbnail = models.ImageField(upload_to='shop/images', default="")

    def __str__(self):
        return self.title


class Subscribe(models.Model):
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.email


class Order(models.Model):
    id = models.IntegerField(primary_key=True, serialize=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    mobile = models.CharField(max_length=10)
    order_Items = jsonfield.JSONField()
    itemLen = jsonfield.JSONField()
    price = jsonfield.JSONField()
    amount = models.IntegerField(default=0)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=15)
    payment_method = models.CharField(max_length=15, default="COD")
    date = models.DateField(auto_now=True , auto_now_add=False)

    def __str__(self):
        return f"ID : {self.id} | Items : {self.order_Items}"
