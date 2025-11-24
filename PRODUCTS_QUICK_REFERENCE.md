# PookieCare Products App - Quick Reference

## Database Models Summary

### Brand
- **Primary Key**: `brand_id` (UUID)
- **Fields**: `brand_name` (unique)
- **Relations**: One-to-Many with Product

### Category
- **Primary Key**: `category_id` (UUID)
- **Fields**: `category_name` (unique)
- **Relations**: One-to-Many with Product

### Product
- **Primary Key**: `product_id` (UUID)
- **Fields**: 
  - `product_name`
  - `product_image` (stored in `media/products/images/`)
  - `product_details` (HTML-supported)
  - `price` (Decimal, in BDT)
  - `available_stock` (Integer)
  - `featured` (Boolean)
- **Relations**: 
  - Many-to-One with Brand
  - Many-to-One with Category

### Order
- **Primary Key**: `order_id` (UUID)
- **Fields**:
  - `in_cart` (Boolean - True: cart, False: completed)
  - `completed_at` (DateTime, nullable)
- **Relations**:
  - Many-to-One with User
  - One-to-Many with OrderItem

### OrderItem
- **Primary Key**: `order_item_id` (UUID)
- **Fields**:
  - `quantity` (Integer)
  - `price_at_purchase` (Decimal - price snapshot)
- **Relations**:
  - Many-to-One with Order
  - Many-to-One with Product
- **Constraints**: Unique together (order, product)

## Key Methods

### Product Methods
```python
product.is_in_stock()         # Returns True if stock > 0
product.get_stock_status()    # Returns: "In Stock", "Low Stock (5 left)", or "Out of Stock"
```

### Order Methods
```python
order.get_total_items()       # Sum of all item quantities
order.get_total_price()       # Sum of all item subtotals
order.complete_order()        # Validates stock, updates inventory, returns True/False
```

### OrderItem Methods
```python
order_item.get_subtotal()     # quantity × price_at_purchase
```

## Shopping Cart Flow

1. **User adds product to cart**:
   ```python
   # Get or create cart order
   order, created = Order.objects.get_or_create(user=user, in_cart=True)
   
   # Add or update order item
   item, created = OrderItem.objects.get_or_create(
       order=order,
       product=product,
       defaults={'quantity': 1}
   )
   if not created:
       item.quantity += 1
       item.save()
   ```

2. **View cart**:
   ```python
   cart = Order.objects.filter(user=user, in_cart=True).first()
   items = cart.items.all() if cart else []
   total = cart.get_total_price() if cart else 0
   ```

3. **Complete order**:
   ```python
   cart = Order.objects.get(user=user, in_cart=True)
   if cart.complete_order():
       # Success - stock updated, order marked as completed
       pass
   else:
       # Failed - insufficient stock
       pass
   ```

## Admin Panel URLs

- **Brands**: `/admin/products/brand/`
- **Categories**: `/admin/products/category/`
- **Products**: `/admin/products/product/`
- **Orders**: `/admin/products/order/`
- **Order Items**: `/admin/products/orderitem/`

## Quick Examples

### Create Brand & Category
```python
from products.models import Brand, Category

brand = Brand.objects.create(brand_name="CeraVe")
category = Category.objects.create(category_name="Moisturizers")
```

### Create Product
```python
from products.models import Product
from decimal import Decimal

product = Product.objects.create(
    product_name="CeraVe Moisturizing Cream",
    brand=brand,
    category=category,
    product_details="<p>Rich, non-greasy moisturizing cream</p>",
    price=Decimal("1250.00"),
    available_stock=50,
    featured=True
)
# Don't forget to upload an image via admin!
```

### Query Products
```python
# All products
products = Product.objects.all()

# Featured products
featured = Product.objects.filter(featured=True)

# Products by brand
cerave_products = Product.objects.filter(brand__brand_name="CeraVe")

# Products in stock
in_stock = Product.objects.filter(available_stock__gt=0)

# Low stock products
low_stock = Product.objects.filter(available_stock__lt=10, available_stock__gt=0)
```

### Query Orders
```python
# User's current cart
cart = Order.objects.filter(user=user, in_cart=True).first()

# User's completed orders
completed_orders = Order.objects.filter(user=user, in_cart=False)

# All active carts
all_carts = Order.objects.filter(in_cart=True)

# Recent orders
recent_orders = Order.objects.filter(in_cart=False).order_by('-completed_at')[:10]
```

## File Upload Notes

### Product Images
- **Upload Path**: Automatically saved to `media/products/images/`
- **Access URL**: `/media/products/images/filename.jpg`
- **Supported Formats**: JPEG, PNG, GIF, WebP
- **Requirements**: Pillow library (already installed)

### In Development
Images are served by Django automatically when `DEBUG=True`

### In Production
Configure your web server to serve `/media/` directly:

**Nginx example**:
```nginx
location /media/ {
    alias /path/to/pookiecare/media/;
}
```

## Common Admin Tasks

### Adding a New Product
1. Login to admin panel
2. Go to Products → Add Product
3. Fill in all required fields
4. Upload product image
5. Set stock quantity
6. Save

### Managing Inventory
1. Go to Products → Products
2. View stock status (color-coded)
3. Click product to edit
4. Update `available_stock` field
5. Save

### Processing Orders
1. Go to Orders → Orders
2. Filter by "In cart: Yes" to see active carts
3. Click order to view details
4. Review order items
5. Use "Complete selected orders" action or mark `in_cart` as False
6. Stock automatically updates

### Viewing Order History
1. Go to Orders → Orders
2. Filter by "In cart: No"
3. View completed orders with timestamps
4. Search by user email or order ID

## Testing

Run tests:
```bash
python manage.py test products
```

All tests (26 total):
```bash
python manage.py test
```

## Next Steps

1. Build product listing page for customers
2. Create product detail pages
3. Implement add-to-cart functionality
4. Build shopping cart UI
5. Create checkout process
6. Integrate payment gateway
7. Add order confirmation emails
8. Implement product search and filters
