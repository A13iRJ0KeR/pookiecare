# Products Application - PookieCare

## Overview
This is the products management application for PookieCare, a skincare e-commerce platform. It handles product catalog, brands, categories, shopping cart, and order management.

## Features

### 1. Brand Management
- **Brand ID**: Automatically generated UUID (Primary Key)
- **Brand Name**: Unique brand identifier
- **Product Relationship**: One-to-many relationship with products
- **Timestamps**: Created and updated timestamps

### 2. Category Management
- **Category ID**: Automatically generated UUID (Primary Key)
- **Category Name**: Unique category identifier
- **Product Relationship**: One-to-many relationship with products
- **Timestamps**: Created and updated timestamps

### 3. Product Management
- **Product ID**: Automatically generated UUID (Primary Key)
- **Product Name**: Name of the skincare product
- **Product Image**: 
  - ImageField supporting both local and network images
  - Local images stored in: `media/products/images/`
  - File structure: `MEDIA_ROOT/products/images/filename.jpg`
- **Brand**: Foreign key relationship to Brand model
- **Category**: Foreign key relationship to Category model
- **Product Details**: HTML-supported rich text for detailed descriptions
- **Price**: Decimal field for product price in BDT (Bangladeshi Taka)
- **Available Stock**: Integer field for inventory management
- **Featured**: Boolean flag to highlight products on homepage
- **Timestamps**: Created and updated timestamps
- **Helper Methods**:
  - `is_in_stock()`: Check if product is available
  - `get_stock_status()`: Return human-readable stock status

### 4. Order Management
- **Order ID**: Automatically generated UUID (Primary Key)
- **User**: Foreign key relationship to User model
- **In Cart**: Boolean flag (True = items in cart, False = order completed)
- **Order Items**: Many-to-many relationship with products through OrderItem
- **Timestamps**: Created, updated, and completed timestamps
- **Helper Methods**:
  - `get_total_items()`: Calculate total quantity of items
  - `get_total_price()`: Calculate total order price
  - `complete_order()`: Process order and update inventory

### 5. OrderItem (Junction Model)
- **Order Item ID**: Automatically generated UUID (Primary Key)
- **Order**: Foreign key relationship to Order
- **Product**: Foreign key relationship to Product
- **Quantity**: Number of items per product
- **Price at Purchase**: Stores product price at time of adding to cart
- **Timestamps**: Created and updated timestamps
- **Helper Methods**:
  - `get_subtotal()`: Calculate subtotal for the item
- **Unique Constraint**: One product per order (quantity can be updated)

## Image Storage

### Local Images
Product images are stored locally using Django's `ImageField`:

**Storage Path**: `media/products/images/`

**Full Path**: `<PROJECT_ROOT>/media/products/images/`

**Example**:
```
pookiecare/
├── media/
│   └── products/
│       └── images/
│           ├── moisturizer-001.jpg
│           ├── sunscreen-spf50.png
│           └── serum-vitamin-c.jpg
```

**URL Access**: 
- Development: `http://127.0.0.1:8000/media/products/images/moisturizer-001.jpg`
- Production: Configure your web server to serve media files

### Network Images
While the ImageField is designed for local storage, you can:
1. Download network images and save them locally
2. Use a custom field or store URLs in a separate CharField if needed
3. Use Django storage backends for cloud storage (AWS S3, Google Cloud Storage, etc.)

## Database Relationships

```
Brand ──────┐
            │
            ├──> Product ──────> OrderItem ──────> Order ──────> User
            │
Category ───┘
```

### Relationship Details:
- **Brand → Product**: One-to-Many (One brand can have many products)
- **Category → Product**: One-to-Many (One category can have many products)
- **Product → OrderItem**: One-to-Many (One product can be in many order items)
- **Order → OrderItem**: One-to-Many (One order can have many items)
- **User → Order**: One-to-Many (One user can have many orders)

## Shopping Cart Logic

### How It Works:

1. **Adding to Cart**:
   - Create an Order with `in_cart=True` (if user doesn't have an active cart)
   - Add OrderItem with product and quantity
   - Price is captured at the time of adding to cart

2. **Cart Items**:
   - Filter orders where `in_cart=True` for the logged-in user
   - Display all OrderItems associated with that order

3. **Completing Order**:
   - Call `order.complete_order()` method
   - Stock validation: Checks if sufficient stock is available
   - Stock update: Decreases `available_stock` by quantity ordered
   - Order status: Sets `in_cart=False` and records `completed_at` timestamp

4. **Order History**:
   - Filter orders where `in_cart=False` for completed orders

## Admin Panel Features

### Brand Admin
- List view with product count
- Search by brand name
- Create/edit brands

### Category Admin
- List view with product count
- Search by category name
- Create/edit categories

### Product Admin
- Comprehensive list view with brand, category, price, stock status
- Color-coded stock status (Red: Out of Stock, Orange: Low Stock, Green: In Stock)
- Image preview in detail view
- Filter by brand, category, featured status
- Search by product name, brand, category
- Mark products as featured
- Rich text editor for product details (HTML supported)

### Order Admin
- List view with user, status, total items, total price
- Color-coded status (Orange: In Cart, Green: Completed)
- Inline OrderItem editing
- Filter by status and dates
- Search by order ID, user email, user name
- Admin action to complete multiple orders at once
- Automatic stock validation

### OrderItem Admin
- List view with order status, product, quantity, pricing
- Automatic subtotal calculation
- Search by product name, order ID, user email

## Usage Example

### Creating Products:
```python
from products.models import Brand, Category, Product

# Create a brand
brand = Brand.objects.create(brand_name="CeraVe")

# Create a category
category = Category.objects.create(category_name="Moisturizers")

# Create a product
product = Product.objects.create(
    product_name="CeraVe Moisturizing Cream",
    product_image="path/to/image.jpg",
    brand=brand,
    category=category,
    product_details="<p>Rich moisturizing cream for dry skin.</p>",
    price=1250.00,
    available_stock=50,
    featured=True
)
```

### Adding to Cart:
```python
from products.models import Order, OrderItem, Product
from django.contrib.auth import get_user_model

User = get_user_model()

# Get user and product
user = User.objects.get(email="customer@example.com")
product = Product.objects.get(product_name="CeraVe Moisturizing Cream")

# Get or create cart order
order, created = Order.objects.get_or_create(
    user=user,
    in_cart=True
)

# Add item to cart
order_item, created = OrderItem.objects.get_or_create(
    order=order,
    product=product,
    defaults={'quantity': 1}
)

if not created:
    # If item already exists, increase quantity
    order_item.quantity += 1
    order_item.save()
```

### Completing Order:
```python
# Get cart order
order = Order.objects.get(user=user, in_cart=True)

# Complete the order
if order.complete_order():
    print("Order completed successfully!")
    print(f"Total: ৳{order.get_total_price():,.2f}")
else:
    print("Order failed due to insufficient stock")
```

## Configuration Required

### settings.py

Add to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ... other apps
    'products',
]
```

Add media files configuration:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

Install Pillow for image handling:
```bash
pip install Pillow
```

### urls.py (Main project)

Add media files serving in development:
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your patterns
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Models Summary

| Model | Primary Key | Key Fields | Relationships |
|-------|-------------|------------|---------------|
| Brand | brand_id (UUID) | brand_name | → products (One-to-Many) |
| Category | category_id (UUID) | category_name | → products (One-to-Many) |
| Product | product_id (UUID) | product_name, price, stock | ← brand, ← category, → order_items |
| Order | order_id (UUID) | user, in_cart | ← user, → items (through OrderItem) |
| OrderItem | order_item_id (UUID) | quantity, price_at_purchase | ← order, ← product |

## Notes

- All models use UUID as primary keys for better security
- Stock management is automatic on order completion
- Price is captured at cart addition time (protects against price changes)
- Orders with `in_cart=True` represent active shopping carts
- Orders with `in_cart=False` represent completed orders
- Unique constraint on OrderItem prevents duplicate products in same order
- Admin panel provides complete e-commerce management interface
