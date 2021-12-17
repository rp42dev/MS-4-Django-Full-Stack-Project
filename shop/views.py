"""
Shop app views
    1. A view to the shop page
        With a query, sorting an search functions
    2. A view to the shop individual item page
        Return single item by id to the template
        Filter query to return reladed by style products
    3. A view to add items to the store
        Return Product form field information to the template
        Post and add new item o the Product model
    4. A view for updating the existing items
        Returning form field information to the template
        Post updated information and update Product model
    5. A view for deleting item from Product
        Get single item by id in Post method
        Delete item from Product model and return to the store page
"""


from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.db.models import F

from .models import Product, Category
from .forms import ItemForm, OrderStatusForm
from checkout.models import Order


def shop(request):
    """A view to return the shop page
    Queries by product category, style
    Product sort functionality name, price
    ascending order or descending order
    """
    products = Product.objects.all().order_by('-id')
    style_list = Product.objects.values('style').distinct()
    categories = Category.objects.all()
    category = 'all'
    sort_name = None
    sortkey = None
    style = 'all'
    query = 'None'
    shop = True

    if request.GET:
        if 'search' in request.GET:
            # Search by keyword in titles and description
            query = request.GET['search']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('shop'))
            queries = Q(name__icontains=query)\
                | Q(description__icontains=query)
            products = products.filter(queries)
            if not products:
                messages.error(
                    request, f'Did not find {query}\
                        in the store. Try somthing else')
                return redirect(reverse('shop'))

        if 'category' in request.GET:
            # Sort by category
            category = request.GET['category']
            if category == 'sale':
                products = products.filter(sale=True)
            elif category == 'all':
                products = products.all()
            else:
                products = products.filter(category__name=category)

        if 'style' in request.GET:
            # Sort by style
            style = request.GET['style']
            if style != 'all':
                products = products.filter(style=style)

        if 'sort' in request.GET:
            # Srot by name, price ASC and DESC
            sortkey = request.GET['sort']
            if sortkey == 'name_asc':
                sort_name = 'Name (A-Z)'
                products = products.order_by('name')
            elif sortkey == 'name_desc':
                sort_name = 'Name (Z-A)'
                products = products.order_by('-name')
            elif sortkey == 'price_asc':
                sort_name = 'Price (L-H)'
                products = products.order_by('price')
            elif sortkey == 'price_desc':
                sort_name = 'Price (H-L)'
                products = products.order_by('-price')

    context = {
        'style_list': style_list,
        'categories': categories,
        'sort_name': sort_name,
        'products': products,
        'sortkey': sortkey,
        'cat': category,
        'style': style,
        'shop': shop,
    }
    return render(request, 'shop/shop.html', context)


def shop_item(request, item_id):
    """
    A view to return the shop item detailed page
    Return related products by style to the template
    """
    cart = request.session.get('cart', {})
    item = get_object_or_404(Product, pk=item_id)

    availability = item.item_count

    if item_id in list(cart.keys()):
        availability = item.item_count - cart[item_id]
    
    related = Product.objects.filter(style=item.style).order_by('-id')
    context = {
        'item': item,
        'related': related,
        'availability': availability,

    }
    return render(request, 'shop/shop_item.html', context)


@login_required
def add_item(request):
    """
    Add items to the store requeres 
    login and superuser privileges
    Get for field date to template
    POST the form field data and save
    """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry only store owners can do that')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            messages.success(request, 'Successfuly added new Item!')
            return redirect(reverse('shop_item', args=[item.id]))
        else:
            messages.error(request, 'Failed so add Item.\
                Please ensure the form is valid.')
    else:
        form = ItemForm()

    context = {
        'form': form,
    }

    return render(request, 'admin/add.html', context)


@login_required
def edit_item(request, item_id):
    """
    Edit items from the store requeres
    login and superuser privileges
    Get for field date to template
    POST the form field data and save
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry only store owners can do that')
        return redirect(reverse('home'))

    item = get_object_or_404(Product, pk=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated item!')
            return redirect(reverse('shop_item', args=[item.id]))
        else:
            messages.error(request, 'Failed to update item.\
                Please ensure the form is valid.')
    else:
        form = ItemForm(instance=item)
        messages.info(request, f'You are editing {item.name}')

    context = {
        'form': form,
        'item': item,
    }

    return render(request, 'admin/edit.html', context)


@login_required
def delete_item(request, item_id):
    """
    Delete an item from the store
    requeres login and superuser privileges
    Submit POST to trigger delete_item function
    Delete permanently item from Product models
    """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry only store owners can do that')
        return redirect(reverse('home'))

    item = get_object_or_404(Product, pk=item_id)

    item.delete()
    messages.success(request, f'Successfully Deleted the {item.name}!')

    return redirect(reverse('shop'))


@login_required
def admin_view(request):
    """
    Administrator management view. Requeres login and
    superuser privileges. Returns low stock products,
    Order status items and product discount items
    """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry only store owners can do that')
        return redirect(reverse('home'))
    else:
        low_stock = Product.objects.filter(
            item_count__lte=5).exclude(item_count=0)
        out_of_stock = Product.objects.filter(item_count=0)
        sale = Product.objects.filter(sale=True)
        orders = Order.objects.all()

        context = {
            'out_of_stock': out_of_stock,
            'low_stock': low_stock,
            'orders': orders,
            'sale': sale,
        }
        return render(request, 'admin/admin.html', context)


@login_required
def order_details(request, order_number):
    """
    A view to order detailed view history
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry only store owners can do that')
        return redirect(reverse('home'))
    else:
        order = get_object_or_404(Order, order_number=order_number)
        form = OrderStatusForm(instance=order)
        if request.POST:
            form = OrderStatusForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
            messages.success(request, 'Successfully updated order Status!')

        template = 'checkout/checkout_success.html'
        context = {
            'order': order,
            'admin': True,
            'form': form,
        }

        return render(request, template, context)

