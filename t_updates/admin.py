from django.contrib import admin
from .models import  Blogpost, Order, Product, Subscribe, Wishlist , Cart
from import_export.admin import ImportExportModelAdmin

@admin.register(Product)
@admin.register(Order)
@admin.register(Wishlist)
@admin.register(Cart)
@admin.register(Blogpost)
@admin.register(Subscribe)
class ModelAdmin(ImportExportModelAdmin):
       pass