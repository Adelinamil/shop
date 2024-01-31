from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from shop.models import ProductCategory, Product


# Create your views here.


def index(request, page=1, category_slug=None):
    category = None
    message = None
    categories = ProductCategory.objects.all()
    sort = None
    direction = 'ASC'
    if 'sort' in request.GET:
        sort = request.GET['sort']
    if 'direction' in request.GET:
        direction = request.GET['direction']

    object_list = Product.objects.filter(amount__gt=0).all()
    if sort in ('name', 'price', 'country', 'created_at'):
        object_list = object_list.order_by(f"{'' if direction == 'ASC' else '-'}{sort}")
    if category_slug:
        category = get_object_or_404(ProductCategory, slug=category_slug)
        object_list = object_list.filter(category=category)

    if object_list.count() == 0:
        message = 'Нет доступных продуктов'

    paginator = Paginator(object_list, per_page=12)
    page_object = paginator.get_page(page)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page)

    return render(
        request, 'shop/index.html',
        {
            'products': page_object,
            'categories': categories,
            'category': category,
            'message': message,
            'current_page': page,
            'sort': sort,
            'current_direction': direction,
            'next_direction': 'DESC' if direction == 'ASC' else 'ASC',
        }
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, amount__gt=0)
    return render(request, 'shop/detail.html', {'product': product})


def where(request):
    return render(request, 'shop/where.html')
