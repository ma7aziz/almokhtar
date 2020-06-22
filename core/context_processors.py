from .models import Cart ,Product

def add_variable_to_context(request):
    cart = Cart.objects.all().filter(
        session=request.session.session_key, is_ordered=False).first()

    featured = Product.objects.all().filter(featured=True)
    print(featured)
    return {
        'cart': cart,
        'featured':featured

    }