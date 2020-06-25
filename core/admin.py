from django.contrib import admin

from .models import Product, Cart_item, Cart , Order , Customer
# Register your models here.


class PoroductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'featured','price' , 'sale_price' ,)
    list_display_links = ('id','title')
    list_editable = ('featured', 'price', 'sale_price')
    list_filter =('featured',)
    list_per_page = 20


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id' , 'customer', 'price', 'timestamp' , 'delivered')
    list_display_links = ('id', 'customer')
    list_editable = ('delivered',)
    list_filter =('delivered',)

admin.site.register(Product , PoroductAdmin)
# admin.site.register(Cart)
# admin.site.register(Cart_item)
admin.site.register(Order , OrderAdmin)
# admin.site.register(Customer)