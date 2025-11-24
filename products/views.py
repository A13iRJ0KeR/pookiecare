from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Product, Brand, Category, Order, OrderItem
from .forms import CheckoutForm


def home_view(request):
    """Display homepage with all products and featured products."""
    products = Product.objects.filter(available_stock__gt=0).select_related('brand', 'category')
    featured_products = products.filter(featured=True)[:6]
    cart_item_count = 0

    if request.user.is_authenticated:
        cart = (
            Order.objects.filter(user=request.user, in_cart=True)
            .prefetch_related('items')
            .first()
        )
        if cart:
            cart_item_count = cart.get_total_items()
    
    # Get filter parameters
    brand_filter = request.GET.get('brand')
    category_filter = request.GET.get('category')
    
    # Apply filters
    if brand_filter:
        products = products.filter(brand__brand_id=brand_filter)
    if category_filter:
        products = products.filter(category__category_id=category_filter)
    
    # Get all brands and categories for filter dropdown
    brands = Brand.objects.all()
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'featured_products': featured_products,
        'brands': brands,
        'categories': categories,
        'selected_brand': brand_filter,
        'selected_category': category_filter,
        'cart_item_count': cart_item_count,
    }
    
    return render(request, 'products/home.html', context)


def product_detail_view(request, product_id):
    """Display detailed product information."""
    product = get_object_or_404(Product, product_id=product_id)
    related_products = Product.objects.filter(
        category=product.category,
        available_stock__gt=0
    ).exclude(product_id=product_id)[:4]
    cart_item_count = 0

    if request.user.is_authenticated:
        cart = (
            Order.objects.filter(user=request.user, in_cart=True)
            .prefetch_related('items')
            .first()
        )
        if cart:
            cart_item_count = cart.get_total_items()
    
    context = {
        'product': product,
        'related_products': related_products,
        'cart_item_count': cart_item_count,
    }
    
    return render(request, 'products/product_detail.html', context)


@login_required
def add_to_cart_view(request, product_id):
    """Add a product to the authenticated user's cart."""
    product = get_object_or_404(Product, product_id=product_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1

    quantity = max(quantity, 1)
    next_url = request.POST.get('next') or reverse('products:home')

    if product.available_stock <= 0:
        messages.error(request, "This product is currently out of stock.")
        return redirect(next_url)

    if quantity > product.available_stock:
        messages.error(request, "Requested quantity exceeds available stock.")
        return redirect(next_url)

    order, _ = Order.objects.get_or_create(user=request.user, in_cart=True)
    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={
            'quantity': quantity,
            'price_at_purchase': product.price,
        }
    )

    if created:
        messages.success(request, f"Added {quantity} x {product.product_name} to your cart.")
    else:
        new_quantity = order_item.quantity + quantity
        if new_quantity > product.available_stock:
            messages.error(
                request,
                f"Only {product.available_stock} items available. Update quantity in cart."
            )
            return redirect(next_url)
        order_item.quantity = new_quantity
        order_item.save()
        messages.success(request, f"Updated {product.product_name} quantity in your cart.")

    return redirect(next_url)


@login_required
def cart_view(request):
    """Display the current user's shopping cart."""
    cart = (
        Order.objects.filter(user=request.user, in_cart=True)
        .prefetch_related('items__product__brand', 'items__product__category')
        .first()
    )
    items = cart.items.all() if cart else []
    total_price = cart.get_total_price() if cart else 0

    return render(
        request,
        'products/cart.html',
        {
            'cart': cart,
            'items': items,
            'total_price': total_price,
        }
    )


@login_required
def update_cart_item_view(request, order_item_id):
    """Update the quantity of a cart item or remove it if quantity < 1."""
    order_item = get_object_or_404(
        OrderItem,
        order_item_id=order_item_id,
        order__user=request.user,
        order__in_cart=True,
    )

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        order_item.delete()
        messages.success(request, "Item removed from your cart.")
        return redirect('products:cart')

    if quantity > order_item.product.available_stock:
        messages.error(request, "Requested quantity exceeds available stock.")
        return redirect('products:cart')

    order_item.quantity = quantity
    order_item.save()
    messages.success(request, "Cart updated.")
    return redirect('products:cart')


@login_required
def remove_from_cart_view(request, order_item_id):
    """Remove an item from the cart."""
    order_item = get_object_or_404(
        OrderItem,
        order_item_id=order_item_id,
        order__user=request.user,
        order__in_cart=True,
    )
    order_item.delete()
    messages.success(request, "Item removed from your cart.")
    return redirect('products:cart')


@login_required
def checkout_view(request):
    """Display order form and complete the order."""
    cart = (
        Order.objects.filter(user=request.user, in_cart=True)
        .prefetch_related('items__product')
        .first()
    )

    if not cart or cart.get_total_items() == 0:
        messages.info(request, "Your cart is empty.")
        return redirect('products:home')

    user = request.user
    initial_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone_number': user.phone_number,
        'house_number': user.house_number,
        'road_number': user.road_number,
        'postal_code': user.postal_code,
        'district': user.district,
    }

    if request.method == 'POST':
        form = CheckoutForm(request.POST, initial=initial_data)
        if form.is_valid():
            # Update user's shipping/contact info for reuse
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.phone_number = form.cleaned_data['phone_number']
            user.house_number = form.cleaned_data['house_number']
            user.road_number = form.cleaned_data['road_number']
            user.postal_code = form.cleaned_data['postal_code']
            user.district = form.cleaned_data['district']
            user.save()

            success = cart.complete_order()
            if success:
                messages.success(request, "Order placed successfully!")
                return redirect('products:home')
            messages.error(request, "Not enough stock to complete your order.")
            return redirect('products:cart')
    else:
        form = CheckoutForm(initial=initial_data)

    return render(
        request,
        'products/checkout.html',
        {
            'cart': cart,
            'items': cart.items.all(),
            'total_price': cart.get_total_price(),
            'form': form,
        }
    )
