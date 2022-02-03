from django.contrib import admin
from .models import Address, Blogpost, Product, Wishlist , Cart
from import_export.admin import ImportExportModelAdmin

@admin.register(Product)
@admin.register(Address)
@admin.register(Wishlist)
@admin.register(Cart)
@admin.register(Blogpost)
class ModelAdmin(ImportExportModelAdmin):
       pass