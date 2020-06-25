from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name = 'index'),
    path('shop', views.shop, name='shop'),
    path('cart', views.cart,name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('product/<int:id>', views.product, name = 'product'),
    path('remove_cart/<int:id>', views.remove_cart, name = 'remove_cart'),
    path('minus_cart', views.minus_cart, name ='minus_cart'),
    path('place_order', views.place_order, name='place_order'),
    path('search', views.search, name='search'),
    path('order', views.order),
    path('contact', views.contact, name='contact'),
    path('orders', views.orders, name = 'orders'),
    path('order/<int:id>',views.order_details, name = 'order_details')
]