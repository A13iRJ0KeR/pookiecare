from django.shortcuts import render, get_object_or_404
from .models import Product, Brand, Category


def home_view(request):
    """Display homepage with all products and featured products."""
    products = Product.objects.filter(available_stock__gt=0).select_related('brand', 'category')
    featured_products = products.filter(featured=True)[:6]
    
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
    }
    
    return render(request, 'products/home.html', context)


def product_detail_view(request, product_id):
    """Display detailed product information."""
    product = get_object_or_404(Product, product_id=product_id)
    related_products = Product.objects.filter(
        category=product.category,
        available_stock__gt=0
    ).exclude(product_id=product_id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    
    return render(request, 'products/product_detail.html', context)
