from django.contrib.auth.decorators import login_required
from django.core.exceptions import BadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST

from cart.models import Cart, CartItem
from shop.models import Product


@login_required
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.total_price() for item in cart_items)
    return render(
        request,
        'cart/cart_detail.html',
        {'cart_items': cart_items, 'total_price': total_price}
    )


@login_required
@require_POST
def cart_add(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id, amount__gt=0)
    try:
        cart_item = cart.items.get(product=product)
    except CartItem.DoesNotExist:
        CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
    else:
        if product.amount - (cart_item.quantity + 1) >= 0:
            cart_item.quantity += 1
            cart_item.save()
        else:
            raise BadRequest('Не хватает единиц на складе')

    return redirect('cart:cart_detail')


@login_required
@require_POST
def cart_remove(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = cart.items.get(product=product)
    except CartItem.DoesNotExist:
        pass
    else:
        if cart_item.quantity - 1 <= 0:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()

    return redirect('cart:cart_detail')
