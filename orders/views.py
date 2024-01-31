from io import BytesIO

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import get_template
from xhtml2pdf import pisa

from cart.models import Cart
from orders.forms import OrderForm
from orders.models import Order, OrderItem
from shop.models import Product


@login_required
def create_order(request):
    cart = Cart.objects.get(user=request.user)
    if not cart.items.count() == 0:
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                with transaction.atomic():
                    order = form.save()
                    for item in cart.items.all():
                        product = Product.objects.get(id=item.product.id)
                        if product.amount - item.quantity >= 0:
                            product.amount -= item.quantity
                            quantity = item.quantity
                        else:
                            quantity = product.amount
                            product.amount = 0

                        OrderItem.objects.create(
                            order=order,
                            product=item.product,
                            quantity=quantity,
                            price=item.product.price
                        )
                        item.delete()
                        product.save()
                return redirect('orders:list_orders')
            else:
                messages.error(request, "Не удалось создать заказ, введите корректные данные")
                return redirect('orders:create')

        form = OrderForm(initial={'user': request.user})
        return render(request, 'orders/create.html', {'order_form': form})
    else:
        messages.error(request, 'Корзина пуста')
        return redirect('cart:cart_detail')


@login_required
def list_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/list.html', {'orders': orders})


@login_required
def delete_order(request, o_id):
    order = get_object_or_404(Order, id=o_id)
    if request.method == 'POST':
        order.delete()

    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/list.html', {'orders': orders})


def html_to_pdf(template_src, context_dict=None):
    if context_dict is None:
        context_dict = {}

    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


@login_required
def order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    pdf = html_to_pdf("orders/pdf.html", {"order": order})
    return HttpResponse(pdf, content_type='application/pdf')
