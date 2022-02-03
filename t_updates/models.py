from unicodedata import category
from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()

    def __str__(self):
        return f"Id : {self.id}"


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
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
