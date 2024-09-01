from django.contrib import admin

from .models import Basket, Product, ProductsCategory

# Register your models here.
admin.site.register(ProductsCategory)


# admin.site.register(Product)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'quantity')
    fields = ('name', 'description', ('price', 'quantity'), 'image', 'category')
    search_fields = ('name',)
    ordering = ('name',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity')
    extra = 0
