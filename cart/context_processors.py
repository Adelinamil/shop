from cart.models import Cart


def cart(request):
    try:
        cart_object = Cart.objects.get(user=request.user)
    except TypeError:
        cart_object = None
    return {'cart': cart_object}


def get_total_price_of_cart(request):
    try:
        cart_object = Cart.objects.get(user=request.user)
    except TypeError:
        total_price = None
    else:
        total_price = 0
        for item in cart_object.items.all():
            total_price += item.total_price()
    return {"total_price": total_price}


def get_amount_items(request):
    try:
        cart_object = Cart.objects.get(user=request.user)
    except TypeError:
        amount_items = None
    else:
        amount_items = cart_object.items.count()
    return {"amount_items": amount_items}
