from django.contrib import admin

from .models import Category, Product, Discount, Cart, Profile

# Register your models here.
admin.site.register([Category,
                     Product,
                     Discount,
                     Cart,
                     Profile])
