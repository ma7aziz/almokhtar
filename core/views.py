from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import EmailMultiAlternatives, mail_admins, send_mail , EmailMessage
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import Cart, Cart_item, Customer, Order, Product
from django.template.loader import render_to_string


# Create your views here.


def index(request):
    if not request.session or not request.session.session_key:
        request.session.save()
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

# single product page
def product(request, id):
    product = Product.objects.get(pk=id)
    related = Product.objects.all().filter(featured=True).order_by('-price')[:4]
    return render(request, 'product.html', {'product': product , 'related':related})


# All products
def shop(request):
    products = Product.objects.all()
    paginator = Paginator(products, 21 )
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop.html',{'page_obj': page_obj})

# cart page and add to cart POST request
def cart(request):
    if request.method == 'POST':
        product = Product.objects.get(pk=request.POST['product_id'])
        if request.POST['qty']:
            qty = int(request.POST['qty'])
        
        cart = Cart.objects.all().filter(
            session=request.session.session_key, is_ordered=False).first()
        if cart:
            cart_item = Cart_item.objects.all().filter(
                shopping_cart=cart, item=product).first()
            if cart_item:
                if qty:
                    cart_item.qty += qty
                    cart_item.save()
                    messages.success(request, 'تم اضافة المنتج الي السلة')

                    # messages.success(request, 'لاتمام عملية الشراء <a href="{% url 'cart' %}"> </a>اضغط هنا  <br> تم اضافة المنتج الي السلة')
                else:
                    cart_item.qty += 1
                    cart_item.save()
                    messages.success(request, 'تم اضافة المنتج الي السلة')
            else:
                cart_item = Cart_item(shopping_cart=cart, item=product, qty=qty )
                cart_item.save()
                messages.success(request, 'تم اضافة المنتج الي السلة')
        else:
            cart = Cart(session=request.session.session_key)
            cart.save()
            cart_item = Cart_item(item=product, shopping_cart=cart)
            cart_item.save()
            messages.success(request, 'تم اضافة المنتج الي السلة')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    return render(request, 'cart.html')

#change quantity of items in cart 
def minus_cart(request):
    pass

def remove_cart(request, id):
    cart_item = Cart_item.objects.get(pk=id)
    cart_item.delete()
    messages.success(request, 'تم حذف المنتج من السلة')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



# checkout page
def checkout(request):
    return render(request, 'checkout.html')

def place_order(request):
    cart = Cart.objects.get(pk= request.POST['cart_id'])
    customer = Customer(name=request.POST['name'], address=request.POST['address'], city=request.POST['city'],
    email=request.POST['email'], phone= request.POST['phone'])
    customer.save()
    notes=request.POST['notes']
    price = cart.cart_price() + 25
    order = Order(customer= customer, cart=cart, notes = notes, price=price)
    order.save()
    cart.is_ordered = True
    cart.save()
    msg_html = render_to_string('order_confirm_email.html', {'order':order})
    # send_mail('Almokhtar Trading - Order Confirmation',
    #               f'Your order has been confirmed successfully. \n Order number : {order.id} . \n Our team will reach out to you soon. \n For further assistance please call 01011240195',
    #               settings.EMAIL_HOST_USER,
    #               [request.POST['email']] , html_message=msg_html , fail_silently=False)
    # email_msg = EmailMessage(
    #     subject='New Order', body='We recieved new order , please check your admin panel', 
    #     from_email='admin@almoukhtar-eg.com',  
    #     to=['omar.elmashaly@gmail.com'],)
    # email_msg.send()
    return render(request, 'order_success.html', {'order':order})



def search(request):
    keyword = request.GET.get('s').strip()
    result = Product.objects.filter(title__icontains = keyword)
    return render(request, 'search.html', {'result': result, 'keyword': keyword})

def order(request):

    return render(request, 'order_success.html', {'order':Order.objects.all().first()})


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        messages.success(request, ' تم ارسال رسالتك بنجاح .. سوف نقوم بالتواصل معك في اقرب وقت ')
        # msg_html = render_to_string('emails/new_contact.html', {'name':name , 'email':email , 'phone':phone, 'message':message})
        # subject  = 'رسالة جديدة'
        # text_content = f'تم استلام رسالة جديدة من موقعنا الاليكتروني .. اسم المرسل {name}..رقم التليفون {phone} .. الايميل {email} ,محتوي الرسالة : {message}'
        # html_content = msg_html
        # email_msg = EmailMultiAlternatives(subject, text_content , 'admin@almoukhtar-eg.com', ['ma7moud.aelaziz@gmail.com', ], )
        # email_msg.attach_alternative(html_content, "text/html")
        # email_msg.send()
    return render(request, 'contact-us.html')


@user_passes_test(lambda u: u.is_superuser)
def orders(request):
    orders = Order.objects.all().order_by('-timestamp')
    paginator = Paginator(orders, 15 )
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = orders.count()
    return render(request, 'orders.html' , 
        {'page_obj': page_obj, 
        # 'count': count, 
        # 'prices': orders_prices
        }
    )



@user_passes_test(lambda u: u.is_superuser)
def order_details(request, id):
    order = Order.objects.get(pk=id)
    return render(request, 'order_details.html' , {'order': order})
